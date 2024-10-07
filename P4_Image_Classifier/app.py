from flask import Flask, render_template, request, jsonify
import os
import json
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
    datos = request.get_json()  
    imagen = datos.get('imagen')
    x = datos.get('x')
    y = datos.get('y')
    ancho = datos.get('ancho')
    alto = datos.get('alto')

    nueva_seccion = {
        "imagen": imagen,
        "x": x,
        "y": y,
        "ancho": ancho,
        "alto": alto
    }

    with open(ARCHIVO_SECCIONES, 'r+') as archivo:
        secciones = json.load(archivo)  
        secciones.append(nueva_seccion) 
        archivo.seek(0) 
        json.dump(secciones, archivo, indent=4)  

    print(f"Coordenadas guardadas para la imagen {imagen}: {nueva_seccion}")

    return jsonify({"mensaje": "Coordenadas enviadas y guardadas correctamente"}), 200

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

    # print("hola\n\n\n\n\n\n\n\n")

    # resultado = clas.realizar_analisis(imagen, coordenadas_guardadas, x, y, ancho, alto)
    res = clasificador.analisis(imagen, coordenadas_guardadas, x, y, ancho, alto)

    print(res)

    return jsonify({"mensaje": "Análisis completado"}), 200

if __name__ == '__main__':
    app.run(debug=True)
