import numpy as np
from scipy.spatial.distance import mahalanobis

# Definir las clases y el punto v
c1 = np.array([[0, 1, 0, 3], [0, 2, 3, 0]])
c2 = np.array([[4, 4, 4, 5], [0, 3, 2, 6]])
c3 = np.array([[6, 7, 7, 8], [0, 1, 3, 2]])

v = np.array([3, -4])

# Función para calcular la distancia de Mahalanobis usando scipy
def distancia_mahalanobis(clase, v):
    # Calcular el vector de medias
    mu = np.mean(clase, axis=1)
    
    # Calcular la matriz de covarianza
    S = np.cov(clase, bias=False)  # bias=False para usar el denominador n-1
    
    # Invertir la matriz de covarianza
    S_inv = np.linalg.inv(S)
    
    # Calcular la distancia de Mahalanobis usando scipy
    distancia = mahalanobis(v, mu, S_inv)
    
    print(f"Distancia de Mahalanobis: {distancia}")
    return distancia

# Calcular las distancias para cada clase
distancia_c1 = distancia_mahalanobis(c1, v)
distancia_c2 = distancia_mahalanobis(c2, v)
distancia_c3 = distancia_mahalanobis(c3, v)
