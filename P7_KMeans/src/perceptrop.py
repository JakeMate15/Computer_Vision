import cv2
import numpy as np
import matplotlib.pyplot as plt

def redimensionar_imagen(imagen, max_dim=1000):
    altura, ancho = imagen.shape[:2]
    if max(altura, ancho) > max_dim:
        if altura > ancho:
            escala = max_dim / altura
        else:
            escala = max_dim / ancho
        nuevo_ancho = int(ancho * escala)
        nueva_altura = int(altura * escala)
        imagen_redimensionada = cv2.resize(imagen, (nuevo_ancho, nueva_altura), interpolation=cv2.INTER_AREA)
        return imagen_redimensionada
    return imagen

# Cargar la imagen
imagen = cv2.imread('ex.png')

# Redimensionar la imagen si es necesario
imagen = redimensionar_imagen(imagen, max_dim=500)

puntos = []
clase = []

for y in range(imagen.shape[0]):
    for x in range(imagen.shape[1]):
        color = imagen[y, x]
        if tuple(color) == (92, 0, 202): 
            puntos.append((x, y, 1))
            clase.append(1)
        elif tuple(color) == (0, 202, 98):  
            puntos.append((x, y, 1))
            clase.append(0)

# Separar los puntos por clase
x1 = [p[0] for p, c in zip(puntos, clase) if c == 1]
y1 = [p[1] for p, c in zip(puntos, clase) if c == 1]
x0 = [p[0] for p, c in zip(puntos, clase) if c == 0]
y0 = [p[1] for p, c in zip(puntos, clase) if c == 0]

# Extraer coordenadas para el entrenamiento
x, y, w = zip(*puntos)

iteraciones = 100
W = np.array([0.5, 1, 1], dtype=np.float64)
X = np.array(puntos, dtype=np.float64)
aprendizaje = 2

print("Pesos iniciales:", W)

for i in range(iteraciones):
    clasificados = 0
    for idx, pto in enumerate(X):
        sal = np.dot(pto, W)
        c = clase[idx]
        
        if sal <= 0 and c == 1:
            W = W + aprendizaje * pto
        elif sal > 0 and c == 0:
            W = W - aprendizaje * pto
        else:
            clasificados += 1
    
    if clasificados == len(puntos):
        print(f"Clasificados correctamente en {i + 1} iteraciones")
        print("Pesos finales:", W)
        break
else:
    print("Se alcanzó el número máximo de iteraciones sin clasificar todos los puntos.")

# Crear una malla para graficar la frontera de decisión
xx, yy = np.meshgrid(np.linspace(min(x), max(x), 500), np.linspace(min(y), max(y), 500))
grid = np.c_[xx.ravel(), yy.ravel(), np.ones(xx.size)]
Z = np.dot(grid, W)
Z = Z.reshape(xx.shape)

# Graficar los puntos y la frontera de decisión
fig, ax = plt.subplots(figsize=(8, 6))
ax.contourf(xx, yy, Z, levels=[Z.min(), 0, Z.max()], alpha=0.2, colors=['green', 'red'])
ax.scatter(x1, y1, c='red', label='Clase 1')
ax.scatter(x0, y0, c='green', label='Clase 0')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Puntos clasificados por clase y frontera de decisión')
ax.legend()

# Función para manejar el evento de clic
def onclick(event):
    ix, iy = event.xdata, event.ydata
    if ix is not None and iy is not None:
        punto = np.array([ix, iy, 1])
        salida = np.dot(punto, W)
        clase_predicha = 1 if salida > 0 else 0
        signo = 'positivo' if salida > 0 else 'negativo'
        ecuacion = f"{W[0]:.2f}*x + {W[1]:.2f}*y + {W[2]:.2f} = {salida:.2f} ({signo})"
        print(f"Punto seleccionado: ({ix:.2f}, {iy:.2f})")
        print(f"Salida del perceptrón: {salida:.2f} ({signo})")
        print(f"Ecuación: {ecuacion}")
        print(f"Clase predicha: {clase_predicha}")
        # Marcar el punto seleccionado en la gráfica
        ax.plot(ix, iy, 'bo', markersize=8)
        fig.canvas.draw()

# Conectar la función al evento de clic
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
