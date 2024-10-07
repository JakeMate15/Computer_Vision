import base64
import io
from flask import Flask, render_template, request, jsonify
import os
import json
import cv2
from werkzeug.utils import send_file

import clasificador

app = Flask(__name__)

DIRECTORIO_IMAGENES = os.path.join(app.static_folder, 'imagenes')

@app.route('/')
def index():
    imagenes = os.listdir(DIRECTORIO_IMAGENES)
    # print("Imágenes encontradas:", imagenes) 
    return render_template('index.html', imagenes=imagenes)

ARCHIVO_SECCIONES = 'secciones_guardadas.json'
if not os.path.exists(ARCHIVO_SECCIONES):
    with open(ARCHIVO_SECCIONES, 'w') as archivo:
        json.dump([], archivo)


@app.route('/guardar-coordenadas', methods=['POST'])
def guardar_coordenadas():
    try:
        datos = request.get_json()

        # Validar los datos recibidos
        if not datos:
            return jsonify({"mensaje": "No se han recibido datos"}), 400

        imagen = datos.get('imagen')
        x = int(datos.get('x'))
        y = int(datos.get('y'))
        ancho = int(datos.get('ancho'))
        alto = int(datos.get('alto'))

        if not all([imagen, x, y, ancho, alto]):
            return jsonify({"mensaje": "Datos incompletos para procesar la imagen"}), 400

        nueva_seccion = {
            "imagen": imagen,
            "x": x,
            "y": y,
            "ancho": ancho,
            "alto": alto
        }

        # Guardar las coordenadas en un archivo o base de datos (aquí un archivo JSON)
        with open(ARCHIVO_SECCIONES, 'r+') as archivo:
            secciones = json.load(archivo)
            secciones.append(nueva_seccion)
            archivo.seek(0)
            json.dump(secciones, archivo, indent=4)

        return jsonify({"mensaje": "Coordenadas enviadas y guardadas correctamente"}), 200

    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return jsonify({"mensaje": "Ocurrió un error al guardar las coordenadas"}), 500


@app.route('/limpiar-coordenadas', methods=['POST'])
def limpiar_coordenadas():
    with open(ARCHIVO_SECCIONES, 'w') as archivo:
        json.dump([], archivo)
    print("Coordenadas limpiadas")
    return jsonify({"mensaje": "Secciones eliminadas correctamente"}), 200


@app.route('/analizar-seccion', methods=['POST'])
def procesar():
    datos = request.get_json()
    imagen = datos['imagen']
    x = datos['x']
    y = datos['y']
    ancho = datos['ancho']
    alto = datos['alto']

    with open(ARCHIVO_SECCIONES, 'r') as archivo:
        coordenadas_guardadas = json.load(archivo)

    resAnalisis = clasificador.analisis(imagen, coordenadas_guardadas, x, y, ancho, alto)
    res = resAnalisis.tolist()

    resultados_json = []
    for resultado in res:
        resultado_dict = {
            "mahalanobis_distance": resultado[0],
            "euclidean_distance": resultado[1],
            "probabilidad": resultado[2]
        }
        resultados_json.append(resultado_dict)

    # Devolver la respuesta JSON
    return jsonify({"resultados": resultados_json}), 200

if __name__ == '__main__':
    app.run(debug=True)
