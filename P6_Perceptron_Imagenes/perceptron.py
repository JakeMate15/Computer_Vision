from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def entrenar(W, X, clases, aprendizaje, iteraciones=100):
    for i in range(iteraciones):
        clasificados = 0
        for idx, pto in enumerate(X):
            sal = np.dot(pto, W)
            c = clases[idx]

            prediccion = 1 if sal >= 0 else 0

            if prediccion != c:
                if c == 1:
                    W = W + aprendizaje * pto
                else:
                    W = W - aprendizaje * pto
            else:
                clasificados += 1

        if clasificados == len(X):
            graficar_3d(X, clases, W)
            print(f"Clasificados correctamente en {i + 1} iteraciones")
            return W

    print("No se alcanzó la convergencia en el número máximo de iteraciones.")
    graficar_3d(X, clases, W)
    return W

def graficar_3d(X, clases, W):
    # Asegurarse de que X tenga al menos 3 características (x, y, z)
    if X.shape[1] < 3:
        raise ValueError("Se requieren al menos 3 características para graficar en 3D.")

    X_plot = X[:, :3]  # (x, y, z)
    clases = np.array(clases)

    # Separar las clases
    clase_0 = X_plot[clases == 0]
    clase_1 = X_plot[clases == 1]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Graficar los puntos de cada clase
    ax.scatter(clase_0[:, 0], clase_0[:, 1], clase_0[:, 2], color='red', label='Clase 0')
    ax.scatter(clase_1[:, 0], clase_1[:, 1], clase_1[:, 2], color='blue', label='Clase 1')

    # Crear una malla para el plano de decisión
    # Ecuación del plano: w1*x + w2*y + w3*z + bias = 0
    # Despejando z: z = (-w1*x - w2*y - bias) / w3
    w1, w2, w3, bias = W
    if w3 != 0:
        # Definir los límites para x e y
        x_lim = ax.get_xlim()
        y_lim = ax.get_ylim()
        x_surf, y_surf = np.meshgrid(
            np.linspace(x_lim[0], x_lim[1], 10),
            np.linspace(y_lim[0], y_lim[1], 10)
        )
        z_surf = (-w1 * x_surf - w2 * y_surf - bias) / w3
        ax.plot_surface(x_surf, y_surf, z_surf, color='green', alpha=0.5, label='Plano de Decisión')
    else:
        print("w3 es cero, el plano de decisión no puede ser graficado en función de z.")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Clasificación 3D y Plano de Decisión')
    ax.legend()
    plt.show()

def predecir (individuo, W):
    sal = np.dot(individuo, W)
    print(sal)

    if sal > 0:
        return 1
    else:
        return 0
    # return sal

def analisis(imagen, coordenadas_guardadas, x, y, ancho, alto):
    ruta_imagen = f'static/imagenes/{imagen}'

    imagen = Image.open(ruta_imagen)
    img = np.array(imagen)

    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")

    x = int(x)
    y = int(y)
    ancho = int(ancho)
    alto = int(alto)
    seccionParaAnalizar = img[y:y+alto, x:x+ancho]
    centroide = seccionParaAnalizar.mean(axis = (0, 1))
    # print(centroide)


    if seccionParaAnalizar.size == 0:
        raise ValueError("La sección para analizar es inválida.")

    puntos = []
    clases = []

    c = 0
    for cord in coordenadas_guardadas:
        xG = int(cord['x'])
        yG = int(cord['y'])
        anchoG = int(cord['ancho'])
        altoG = int(cord['alto'])

        region = img[yG:yG+altoG, xG:xG+anchoG]

        for i in range(region.shape[0]):
            for j in range(region.shape[1]):
                x_pto = xG + j
                y_pto = yG + i
                z = region[i, j, 2]
                puntos.append((x_pto, y_pto, z, 1))
                clases.append(c)

        c += 1

    W = np.zeros(len(puntos[0]))
    X = np.array(puntos)
    aprendizaje = 0.2
    centroide = np.append(centroide, 1)

    W = entrenar(W, X, clases, aprendizaje)
    prediccion = predecir(centroide, W)
    print(W)
    print(prediccion + 1)

    return prediccion

