import matplotlib.pyplot as plt
import numpy as np

puntos = [
    (0, 0, 0, 1),
    (1, 0, 0, 1),
    (1, 1, 0, 1),
    (0, 1, 0, 1),
    (0, 0, 1, 1),
    (1, 0, 1, 1),
    (1, 1, 1, 1),
    (0, 1, 1, 1) 
]

clases = [0, 0, 0, 1, 1, 0, 1, 1]
x, y, z, w = zip(*puntos)

def grafica(x, y, z, clases, plano):
    a, b, c, d = plano
    if c == 0:
        print("El coeficiente w3 (c) no puede ser cero para graficar el plano.")
        return 
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for xi, yi, zi, clase in zip(x, y, z, clases):
        color = 'red' if clase == 0 else 'blue'
        ax.scatter(xi, yi, zi, color=color)
        
    xx, yy = np.meshgrid(np.linspace(min(x), max(x), 10), np.linspace(min(y), max(y), 10))
    zz = (-a * xx - b * yy - d) / c
    
    ax.plot_surface(xx, yy, zz, color='green', alpha=0.5)
    
    plt.show()
    
iteraciones = 50
W = np.array([0.5, 1, .2, 1], dtype=np.float64)
X = np.array(puntos, dtype=np.float64)
aprendizaje = 2

print(W)
# grafica(x, y, z, clases, W.tolist())

for i in range(iteraciones):
    print("===========================")
    clasificados = 0
    for idx, pto in enumerate(X):
        sal = np.dot(pto, W)
        c = clases[idx]
        
        if sal <= 0 and c == 0:
            W = W + aprendizaje * pto
        elif sal >= 0 and c == 1:
            W = W - aprendizaje * pto
        else:
            clasificados += 1
        
    print(W)  
    # grafica(x, y, z, clases, W.tolist())
    if clasificados == len(puntos):
        grafica(x, y, z, clases, W.tolist())
        print(f"Clasificados con {i + 1} iteraciones")
        print(W)
        break
       