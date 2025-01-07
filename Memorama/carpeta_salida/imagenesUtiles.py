import re
import os
import shutil

nombres = []
with open('caracteristicas/pares.txt', 'r') as f:
    for linea in f:
        partes = re.split(r'[ =]+', linea.strip())
        for p in partes:
            if ".png" in p:
                nombres.append(p)

print(f"Total de nombres en el archivo: {len(nombres)}")

os.makedirs('tarjetas', exist_ok=True)

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d != 'tarjetas']
    for nombre in nombres:
        if nombre in files:
            origen = os.path.join(root, nombre)
            destino = os.path.join('tarjetas', nombre)
            if os.path.abspath(origen) != os.path.abspath(destino):
                shutil.copy2(origen, destino)

carpeta = 'tarjetas'
archivos_copiados = set(os.listdir(carpeta))

esperados = set(nombres)
print(f"Total de archivos esperados: {len(esperados)}")

faltantes = esperados - archivos_copiados
extras = archivos_copiados - esperados

if not faltantes and not extras:
    print("Todas las imágenes fueron copiadas correctamente.")
else:
    if faltantes:
        print("Imágenes faltantes:")
        for archivo in faltantes:
            print(archivo)
    if extras:
        print("\nImágenes adicionales en la carpeta:")
        for archivo in extras:
            print(archivo)