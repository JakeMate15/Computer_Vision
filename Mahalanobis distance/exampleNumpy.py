import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Definir las clases y el vector v
c1 = np.array([[0, 1, 0, 3], [0, 2, 3, 0]])
c2 = np.array([[4, 4, 4, 5], [0, 3, 2, 6]])
c3 = np.array([[6, 7, 7, 8], [0, 1, 3, 2]])

v = np.array([3, -4])

# Función para calcular la distancia de Mahalanobis usando scipy
def distancia_mahalanobis(clase, v):
    # Calcular el vector de medias
    mu = np.mean(clase, axis=1)
    
    # Calcular la matriz de covarianza
    X_centrado = clase - mu[:, None]  # Centrar los datos
    n = clase.shape[1]  # El número de muestras (columnas)
    S = (1 / n) * np.dot(X_centrado, X_centrado.T)  # Matriz de covarianza
    
    # Invertir la matriz de covarianza
    S_inv = np.linalg.inv(S)
    
    # Calcular la distancia de Mahalanobis
    delta = v - mu
    distancia = distance.mahalanobis(mu, v, S_inv)
    
    return distancia

# Función para calcular el centroide
def calcular_centroide(clase):
    return np.mean(clase, axis=1)

# Función para calcular la distancia euclidiana entre el centroide y el punto
def distancia_euclidiana(clase, punto):
    centroide = calcular_centroide(clase)
    return np.linalg.norm(centroide - punto)

# Calcular las distancias para cada clase
distancia_mahalanobis_c1 = distancia_mahalanobis(c1, v)
distancia_mahalanobis_c2 = distancia_mahalanobis(c2, v)
distancia_mahalanobis_c3 = distancia_mahalanobis(c3, v)

distancia_euclidiana_c1 = distancia_euclidiana(c1, v)
distancia_euclidiana_c2 = distancia_euclidiana(c2, v)
distancia_euclidiana_c3 = distancia_euclidiana(c3, v)

print(f"Distancia de Mahalanobis a C1: {distancia_mahalanobis_c1}")
print(f"Distancia de Mahalanobis a C2: {distancia_mahalanobis_c2}")
print(f"Distancia de Mahalanobis a C3: {distancia_mahalanobis_c3}")

print(f"Distancia Euclidiana a C1: {distancia_euclidiana_c1}")
print(f"Distancia Euclidiana a C2: {distancia_euclidiana_c2}")
print(f"Distancia Euclidiana a C3: {distancia_euclidiana_c3}")

# Graficar las clases
plt.figure(figsize=(10, 7))

# Graficar Clase 1
plt.scatter(c1[0], c1[1], color='red', label='Clase 1')
plt.scatter(calcular_centroide(c1)[0], calcular_centroide(c1)[1], color='red', marker='o', s=100, edgecolor='black', label='Centroide C1')

# Graficar Clase 2
plt.scatter(c2[0], c2[1], color='blue', label='Clase 2')
plt.scatter(calcular_centroide(c2)[0], calcular_centroide(c2)[1], color='blue', marker='o', s=100, edgecolor='black', label='Centroide C2')

# Graficar Clase 3
plt.scatter(c3[0], c3[1], color='green', label='Clase 3')
plt.scatter(calcular_centroide(c3)[0], calcular_centroide(c3)[1], color='green', marker='o', s=100, edgecolor='black', label='Centroide C3')

# Graficar el punto v
plt.scatter(v[0], v[1], color='black', marker='x', s=100, label='Punto v')

plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.legend()
plt.title('Gráfico de Clases y Punto v con Centros')
plt.grid(True)
plt.show()
