import os
import io
import cv2
import numpy as np
from PIL import Image
from rembg import remove
from skimage.measure import label, regionprops

def quitaFondo(ruta):
    with open(ruta, 'rb') as f:
        datos = f.read()
    sin_fondo = remove(datos)
    img = Image.open(io.BytesIO(sin_fondo)).convert("RGBA")
    fondo_negro = Image.new("RGBA", img.size, (0, 0, 0, 255))
    fondo_negro.paste(img, (0, 0), img)
    imagen_final = fondo_negro.convert("RGB")
    return imagen_final

def separaObjetos(imagen, umbral_valor= 10, area_minima=1000):
    imagen_rgb = imagen.convert("RGB")
    imagen_np = np.array(imagen_rgb)  
    
    imagen_cv = cv2.cvtColor(imagen_np, cv2.COLOR_RGB2BGR)
    
    gris = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2GRAY)
    
    _, umbral = cv2.threshold(gris, umbral_valor, 255, cv2.THRESH_BINARY)
    
    kernel = np.ones((3,3), np.uint8)
    umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)
    
    contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    contornos_filtrados = [c for c in contornos if cv2.contourArea(c) > area_minima]
    
    contornos_filtrados = sorted(contornos_filtrados, key=cv2.contourArea, reverse=True)
    contornos_filtrados = contornos_filtrados[:5]
    
    objetos = []
    for contorno in contornos_filtrados:
        x, y, w, h = cv2.boundingRect(contorno)
        roi = imagen_cv[y:y+h, x:x+w]
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(roi_rgb)
        objetos.append(imagen_pil)
    
    return objetos

def objetoIndividual(imagenes, umbral=10):
    resultado = []
    for img in imagenes:
        imagen_gris = img.convert('L')
        imagen_np = np.array(imagen_gris)
        _, binarizada = cv2.threshold(imagen_np, umbral, 255, cv2.THRESH_BINARY)
        contornos, _ = cv2.findContours(binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contornos:
            raise ValueError("No se encontraron objetos en la imagen binarizada.")
        contorno_principal = max(contornos, key=cv2.contourArea)
        mascara = np.zeros_like(binarizada)
        cv2.drawContours(mascara, [contorno_principal], -1, color=255, thickness=-1)
        puntos = cv2.findNonZero(mascara)
        x, y, w, h = cv2.boundingRect(puntos)
        original_np = np.array(img)
        if original_np.ndim == 2:
            objeto = original_np[y:y+h, x:x+w]
            mask_cropped = mascara[y:y+h, x:x+w]
            objeto_recortado = cv2.bitwise_and(objeto, objeto, mask=mask_cropped)
        else:
            objeto = original_np[y:y+h, x:x+w, :]
            mask_cropped = mascara[y:y+h, x:x+w]
            mask_cropped = mask_cropped[:, :, np.newaxis]
            objeto_recortado = cv2.bitwise_and(objeto, objeto, mask=mask_cropped)
        imagen_final = Image.fromarray(objeto_recortado)
        resultado.append(imagen_final)
    return resultado



def procesar_carpeta_principal(carpeta_principal, carpeta_salida='imagenes_extraidas'):
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
    
    for nombre_carpeta in os.listdir(carpeta_principal):
        ruta_carpeta = os.path.join(carpeta_principal, nombre_carpeta)
        if os.path.isdir(ruta_carpeta):
            if nombre_carpeta == 'entrenamietno' or nombre_carpeta == 'imagenes_extraidas' or nombre_carpeta == 'combinaciones':
            # if not (nombre_carpeta == 'combinaciones'):
            # if not (nombre_carpeta == 'cuchillos'):
            # if not (nombre_carpeta == 'cucharas'):
                continue
            print(f"Procesando carpeta: {nombre_carpeta}")
            contador = 1
            
            for archivo in os.listdir(ruta_carpeta):
                ruta_archivo = os.path.join(ruta_carpeta, archivo)
                
                if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    try:
                        # Quitar el fondo
                        imagen_procesada = quitaFondo(ruta_archivo)
                        
                        # Separar objetos
                        objetos = objetoIndividual(separaObjetos(imagen_procesada))
                        
                        # Guardar cada objeto extraído
                        for obj in objetos:
                            nombre_guardado = f"{nombre_carpeta}_{contador}.png"
                            ruta_guardado = os.path.join(carpeta_salida, nombre_guardado)
                            obj.save(ruta_guardado)
                            print(f"Guardado: {ruta_guardado}")
                            contador += 1
                    
                    except Exception as e:
                        print(f"Error procesando {ruta_archivo}: {e}")


carpeta_principal = '/home/erik/Desktop/ESCOM/Computer_Vision/Memorama/carpeta_salida'  # Reemplaza con la ruta real
carpeta_salida = 'entrenamietno'
procesar_carpeta_principal(carpeta_principal, carpeta_salida)
