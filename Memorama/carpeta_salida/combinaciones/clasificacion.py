import os
import io
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from rembg import remove
from skimage.morphology import skeletonize, opening, disk
from skimage.measure import label, regionprops
from sklearn.ensemble import RandomForestClassifier
import joblib

def quitaFondo(ruta):
    with open(ruta, 'rb') as f:
        datos = f.read()
    sin_fondo = remove(datos)
    img = Image.open(io.BytesIO(sin_fondo)).convert("RGBA")
    fondo_negro = Image.new("RGB", img.size, (0, 0, 0))
    fondo_negro.paste(img, (0, 0), img)
    return fondo_negro

def separaObjetos(imagen, umbral_valor=10, area_minima=1000):
    img_np = np.array(imagen)
    gris = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    _, binarizada = cv2.threshold(gris, umbral_valor, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3,3), np.uint8)
    binarizada = cv2.morphologyEx(binarizada, cv2.MORPH_CLOSE, kernel)
    contornos, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_filtrados = [c for c in contornos if cv2.contourArea(c) > area_minima]
    contornos_filtrados = sorted(contornos_filtrados, key=cv2.contourArea, reverse=True)[:5]
    objetos = []
    for contorno in contornos_filtrados:
        x, y, w, h = cv2.boundingRect(contorno)
        roi = img_np[y:y+h, x:x+w]
        objetos.append(Image.fromarray(roi))
    return objetos

def objetoIndividual(imagenes, umbral=10):
    resultado = []
    for img in imagenes:
        img_np = np.array(img)
        if img.mode != 'L':
            gris = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gris = img_np
        _, binarizada = cv2.threshold(gris, umbral, 255, cv2.THRESH_BINARY)
        contornos, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contornos:
            resultado.append(None)
            continue
        contorno_principal = max(contornos, key=cv2.contourArea)
        mascara = np.zeros_like(binarizada)
        cv2.drawContours(mascara, [contorno_principal], -1, 255, -1)
        x, y, w, h = cv2.boundingRect(contorno_principal)
        recorte = img_np[y:y+h, x:x+w].copy()
        sub_mascara = mascara[y:y+h, x:x+w]
        if recorte.ndim == 2:
            objeto_recortado = cv2.bitwise_and(recorte, recorte, mask=sub_mascara)
        else:
            sub_mascara = sub_mascara[:, :, np.newaxis]
            objeto_recortado = cv2.bitwise_and(recorte, recorte, mask=sub_mascara)
        resultado.append(Image.fromarray(objeto_recortado))
    return resultado

def numero_de_terminaciones(skel):
    terminations = 0
    for i in range(1, skel.shape[0]-1):
        for j in range(1, skel.shape[1]-1):
            if skel[i, j] == 1:
                vecinos = skel[i-1:i+2, j-1:j+2]
                cuenta_vecinos = np.sum(vecinos) - 1
                if cuenta_vecinos == 1:
                    terminations += 1
    return terminations

def extraer_caracteristicas_array(img_np):
    if img_np is None or img_np.size == 0:
        return None
    if len(img_np.shape) == 2:
        h, w = img_np.shape
    else:
        h, w = img_np.shape[:2]
    ratio = h / w if w != 0 else 1
    size = (128, 128)
    if ratio > 1:
        new_h = size[0]
        new_w = int(new_h / ratio)
    else:
        new_w = size[1]
        new_h = int(new_w * ratio)
    img_np = cv2.resize(img_np, (new_w, new_h))
    if len(img_np.shape) == 2:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)

    mean_b = np.mean(img_np[:,:,0])
    mean_g = np.mean(img_np[:,:,1])
    mean_r = np.mean(img_np[:,:,2])
    hsv = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)
    mean_h = np.mean(hsv[:,:,0])
    mean_s = np.mean(hsv[:,:,1])
    mean_v = np.mean(hsv[:,:,2])

    gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    thresh_morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    contornos, _ = cv2.findContours(thresh_morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return None
    c = max(contornos, key=cv2.contourArea)
    area = cv2.contourArea(c)
    perimetro = cv2.arcLength(c, True)
    M = cv2.moments(c)
    hu = cv2.HuMoments(M).flatten()

    mask = np.zeros_like(gray, dtype=np.uint8)
    cv2.drawContours(mask, [c], -1, 255, -1)
    mask_open = opening(mask > 0, disk(1))
    skel = skeletonize(mask_open)
    longitud_skel = np.sum(skel)
    term = numero_de_terminaciones(skel)

    lbl = label(mask_open)
    props = regionprops(lbl)
    if not props:
        return None
    r = max(props, key=lambda x: x.area)
    minr, minc, maxr, maxc = r.bbox
    bbox_ratio = (maxc - minc) / (maxr - minr) if (maxr - minr) != 0 else 0
    extent = r.extent
    solidity = r.solidity

    return np.concatenate([
        [mean_r, mean_g, mean_b],
        [mean_h, mean_s, mean_v],
        [area, perimetro],
        hu,
        [longitud_skel, term, bbox_ratio, extent, solidity]
    ])

columnas = ['R', 'G', 'B',
            'H', 'S', 'V',
            'area', 'perimetro',
            'Hu1', 'Hu2', 'Hu3', 'Hu4', 'Hu5', 'Hu6', 'Hu7',
            'longitud_skel', 'terminaciones', 'bbox_ratio', 'extent', 'solidity']

def clasificar_objetos(ruta_imagen, dataset):
    modelo = joblib.load("/home/erik/Desktop/ESCOM/Computer_Vision/Memorama/carpeta_salida/combinaciones/model.pkl")
    imagen_procesada = quitaFondo(ruta_imagen)
    objetos = objetoIndividual(separaObjetos(imagen_procesada))
    res = {}

    for i, obj in enumerate(objetos):
        if obj is None:
            print(f"Objeto {i} en {ruta_imagen}: no se pudo procesar")
            continue

        # Mostrar ventana con el objeto detectado (opcional)
        # obj.show(title=f"Objeto {i}")

        arr = np.array(obj)
        caracteristicas = extraer_caracteristicas_array(arr)
        if caracteristicas is not None:
            # Almacenar las características en el dataset
            dataset.append({
                'imagen': ruta_imagen,
                'objeto_id': i,
                **dict(zip(columnas, caracteristicas))
            })

            # Clasificar el objeto
            prediccion = modelo.predict(pd.DataFrame([caracteristicas], columns=columnas))
            # print(f"Objeto {i} en {ruta_imagen}: clase = {prediccion[0]}")
            if prediccion[0] in res:
                res[prediccion[0]] += 1
            else:
                res[prediccion[0]] = 1
        else:
            print(f"Objeto {i} en {ruta_imagen}: no se pudieron extraer características")
    return res

# Inicializar el dataset
dataset = []

# Obtener la lista de archivos .png en el directorio actual
archivos = sorted([f for f in os.listdir('.') if f.endswith('.png')])

# Procesar cada par de archivos (puedes ajustar esto según tus necesidades)
for i in range(0, len(archivos), 2):
    r1 = clasificar_objetos(archivos[i], dataset)
    r2 = clasificar_objetos(archivos[i + 1], dataset)

    if r1 == r2:
        print(f"{archivos[i]} == {archivos[i + 1]}")
    print((i + 1) / len(archivos))

# Crear el DataFrame a partir del dataset
df = pd.DataFrame(dataset, columns=['imagen', 'objeto_id'] + columnas)

# Guardar el DataFrame en un archivo CSV
df.to_csv('dataset_caracteristicas_combinados.csv', index=False)
print("Dataset guardado en 'dataset_caracteristicas.csv'")