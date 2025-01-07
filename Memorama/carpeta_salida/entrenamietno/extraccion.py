import os
import cv2
import numpy as np
import pandas as pd
from skimage.morphology import skeletonize, opening, disk
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt

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

def extraer_caracteristicas(ruta_imagen):
    img = cv2.imread(ruta_imagen)
    if img is None:
        return None
    h, w = img.shape[:2]
    ratio = h / w if w != 0 else 1
    size = (128, 128)
    if ratio > 1:
        new_h = size[0]
        new_w = int(new_h / ratio)
    else:
        new_w = size[1]
        new_h = int(new_w * ratio)
    img = cv2.resize(img, (new_w, new_h))
    mean_b = np.mean(img[:,:,0])
    mean_g = np.mean(img[:,:,1])
    mean_r = np.mean(img[:,:,2])
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mean_h = np.mean(hsv[:,:,0])
    mean_s = np.mean(hsv[:,:,1])
    mean_v = np.mean(hsv[:,:,2])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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
    plt.figure(figsize=(6,6))
    plt.imshow(skel, cmap='gray')
    plt.axis('off')
    plt.savefig('esqueleto.png')
    return np.concatenate([
        [mean_r, mean_g, mean_b],
        [mean_h, mean_s, mean_v],
        [area, perimetro],
        hu,
        [longitud_skel, term, bbox_ratio, extent, solidity]
    ])

def procesar_dataset(ruta_carpeta, csv_salida='dataset.csv'):
    data = []
    for file in os.listdir(ruta_carpeta):
        if file.endswith('.png'):
            splitted = file.split('_')
            file_class = splitted[0]
            full_path = os.path.join(ruta_carpeta, file)
            features = extraer_caracteristicas(full_path)
            if features is not None:
                data.append(
                    [file, file_class] + features.tolist()
                )
    col_names = [
        'nombre_archivo','clase',
        'R','G','B',
        'H','S','V',
        'area','perimetro',
        'Hu1','Hu2','Hu3','Hu4','Hu5','Hu6','Hu7',
        'longitud_skel','terminaciones','bbox_ratio','extent','solidity'
    ]
    df = pd.DataFrame(data, columns=col_names)
    df.to_csv(csv_salida, index=False)

if __name__ == "__main__":
    procesar_dataset('/home/erik/Desktop/ESCOM/Computer_Vision/Memorama/carpeta_salida/entrenamietno', 'dataset.csv')
