import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

# Definir las clases y el vector v
c1 = np.array([[0, 1, 0, 3], [0, 2, 3, 0]])
c2 = np.array([[4, 4, 4, 5], [0, 3, 2, 6]])
c3 = np.array([[6, 7, 7, 8], [0, 1, 3, 2]])

v = np.array([3, -4])

# Función para calcular la densidad de probabilidad paso a paso
def densidad_probabilidad_paso_a_paso(clase, punto):
    # 1. Calcular el vector de medias (mu)
    mu = np.mean(clase, axis=1)
    print(f"Vector de medias (mu): {mu}")
    
    # 2. Calcular la matriz de covarianza (Sigma)
    X_centrado = clase - mu[:, None]  # Centrar los datos
    n = clase.shape[1]  # Número de muestras
    S = (1 / n) * np.dot(X_centrado, X_centrado.T)  # Matriz de covarianza
    print(f"Matriz de covarianza (Sigma):\n{S}")
    
    # 3. Invertir la matriz de covarianza (Sigma_inv)
    S_inv = np.linalg.inv(S)
    print(f"Inversa de la matriz de covarianza (Sigma_inv):\n{S_inv}")
    
    # 4. Calcular el determinante de la matriz de covarianza (det(Sigma))
    det_S = np.linalg.det(S)
    print(f"Determinante de la matriz de covarianza (det(Sigma)): {det_S}")
    
    # 5. Calcular la distancia cuadrática de Mahalanobis
    delta = punto - mu
    distancia_mahalanobis_squared = np.dot(delta.T, np.dot(S_inv, delta))
    print(f"Distancia cuadrática de Mahalanobis: {distancia_mahalanobis_squared}")
    
    # 6. Calcular la densidad de probabilidad
    n = len(mu)  # Número de características
    densidad = (1 / ( (2 * np.pi) ** (n / 2) * np.sqrt(det_S) )) * np.exp(-0.5 * distancia_mahalanobis_squared)
    print(f"Densidad de probabilidad: {densidad}")
    
    return densidad

# Calcular las densidades de probabilidad para cada clase
print("Clase 1:")
densidad_c1 = densidad_probabilidad_paso_a_paso(c1, v)

print("\nClase 2:")
densidad_c2 = densidad_probabilidad_paso_a_paso(c2, v)

print("\nClase 3:")
densidad_c3 = densidad_probabilidad_paso_a_paso(c3, v)

print('\n\n\n')

print(densidad_c1, densidad_c2, densidad_c3, densidad_c1 + densidad_c2 + densidad_c3)
pv = densidad_c1 + densidad_c2 + densidad_c3
print(pv)

print(densidad_c1 / pv * 100)
print(densidad_c2 / pv * 100)
print(densidad_c3 / pv * 100)
