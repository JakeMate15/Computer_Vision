import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.exceptions import NotFittedError
from typing import Union

class Clasificador:
    """
    Una clase para clasificar puntos utilizando diferentes métodos:
    1. Máxima Probabilidad (Gaussian Naive Bayes)
    2. Distancia de Mahalanobis (K-Nearest Neighbors)
    3. Distancia Euclidiana (K-Nearest Neighbors)
    """

    def __init__(self, X: np.ndarray, y: np.ndarray, n_neighbors: int = 3):
        """
        Inicializa el clasificador con los datos de entrenamiento.

        Parámetros:
        - X: np.ndarray, matriz de características de entrenamiento con 3 características por muestra.
        - y: np.ndarray, vector de etiquetas de entrenamiento.
        - n_neighbors: int, número de vecinos a considerar en KNN.
        """
        if not isinstance(X, np.ndarray):
            raise TypeError("X debe ser un numpy.ndarray.")
        if not isinstance(y, np.ndarray):
            raise TypeError("y debe ser un numpy.ndarray.")
        if X.shape[1] != 3:
            raise ValueError(f"X debe tener exactamente 3 características por muestra, pero tiene {X.shape[1]}.")
        if X.shape[0] != y.shape[0]:
            raise ValueError("El número de muestras en X debe coincidir con el número de etiquetas en y.")

        self.n_neighbors = n_neighbors

        # Escalado de características
        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(X)
        self.y = y

        # Clasificador Gaussian Naive Bayes
        self.gnb = GaussianNB()
        self.gnb.fit(self.X_scaled, self.y)

        # Clasificador KNN con distancia Euclidiana
        self.knn_euclidean = KNeighborsClassifier(n_neighbors=self.n_neighbors, metric='euclidean')
        self.knn_euclidean.fit(self.X_scaled, self.y)

        # Calcular la matriz de covarianza y su inversa para Mahalanobis
        cov_matrix = np.cov(self.X_scaled, rowvar=False)
        try:
            inv_cov_matrix = np.linalg.inv(cov_matrix)
        except np.linalg.LinAlgError:
            # Si la matriz no es invertible, usar pseudo-inversa
            inv_cov_matrix = np.linalg.pinv(cov_matrix)

        # Clasificador KNN con distancia de Mahalanobis (corregido)
        self.knn_mahalanobis = KNeighborsClassifier(
            n_neighbors=self.n_neighbors,
            metric='mahalanobis',
            metric_params={'VI': inv_cov_matrix}
        )
        self.knn_mahalanobis.fit(self.X_scaled, self.y)

    def _validar_punto(self, punto: np.ndarray):
        """
        Valida que el punto sea un numpy.ndarray con exactamente tres elementos.

        Parámetros:
        - punto: np.ndarray, características del punto a clasificar.

        Lanza:
        - TypeError: Si punto no es un numpy.ndarray.
        - ValueError: Si punto no tiene exactamente tres elementos.
        """
        if not isinstance(punto, np.ndarray):
            raise TypeError("El punto debe ser un numpy.ndarray.")
        if punto.shape != (3,):
            raise ValueError(f"El punto debe tener exactamente tres elementos, pero tiene {punto.shape[0]}.")

    def _validar_puntos(self, puntos: np.ndarray):
        """
        Valida que los puntos sean un numpy.ndarray con exactamente tres características.

        Parámetros:
        - puntos: np.ndarray, características de los puntos a clasificar.

        Lanza:
        - TypeError: Si puntos no es un numpy.ndarray.
        - ValueError: Si los puntos no tienen exactamente tres características.
        """
        if not isinstance(puntos, np.ndarray):
            raise TypeError("Los puntos deben ser un numpy.ndarray.")
        if puntos.ndim != 2 or puntos.shape[1] != 3:
            raise ValueError(f"Cada punto debe tener exactamente tres elementos, pero tiene {puntos.shape[1]}.")

    def maxProb(self, puntos: np.ndarray) -> np.ndarray:
        """
        Clasifica múltiples puntos basados en la máxima probabilidad usando Gaussian Naive Bayes.

        Parámetros:
        - puntos: np.ndarray de forma (n_samples, 3), características de los puntos a clasificar.

        Retorna:
        - np.ndarray, etiquetas predichas.
        """
        self._validar_puntos(puntos)
        puntos_scaled = self.scaler.transform(puntos)
        try:
            pred = self.gnb.predict(puntos_scaled)
        except NotFittedError:
            raise Exception("El modelo GaussianNB no está entrenado.")
        return pred

    def distMahalanobis(self, puntos: np.ndarray) -> np.ndarray:
        """
        Clasifica múltiples puntos basados en la distancia de Mahalanobis usando KNN.

        Parámetros:
        - puntos: np.ndarray de forma (n_samples, 3), características de los puntos a clasificar.

        Retorna:
        - np.ndarray, etiquetas predichas.
        """
        self._validar_puntos(puntos)
        puntos_scaled = self.scaler.transform(puntos)
        try:
            pred = self.knn_mahalanobis.predict(puntos_scaled)
        except NotFittedError:
            raise Exception("El modelo KNN con distancia de Mahalanobis no está entrenado.")
        return pred

    def distEuclideana(self, puntos: np.ndarray) -> np.ndarray:
        """
        Clasifica múltiples puntos basados en la distancia Euclidiana usando KNN.

        Parámetros:
        - puntos: np.ndarray de forma (n_samples, 3), características de los puntos a clasificar.

        Retorna:
        - np.ndarray, etiquetas predichas.
        """
        self._validar_puntos(puntos)
        puntos_scaled = self.scaler.transform(puntos)
        try:
            pred = self.knn_euclidean.predict(puntos_scaled)
        except NotFittedError:
            raise Exception("El modelo KNN con distancia Euclidiana no está entrenado.")
        return pred

    def maxProb1(self, punto: np.ndarray) -> Union[int, float]:
        """
        Clasifica un punto basado en la máxima probabilidad usando Gaussian Naive Bayes.

        Parámetros:
        - punto: np.ndarray de tres elementos, características del punto a clasificar.

        Retorna:
        - int o float, etiqueta predicha.
        """
        self._validar_punto(punto)
        punto = punto.reshape(1, -1)
        punto_scaled = self.scaler.transform(punto)
        try:
            pred = self.gnb.predict(punto_scaled)
        except NotFittedError:
            raise Exception("El modelo GaussianNB no está entrenado.")
        return pred[0]

    def distMahalanobis1(self, punto: np.ndarray) -> Union[int, float]:
        """
        Clasifica un punto basado en la distancia de Mahalanobis usando KNN.

        Parámetros:
        - punto: np.ndarray de tres elementos, características del punto a clasificar.

        Retorna:
        - int o float, etiqueta predicha.
        """
        self._validar_punto(punto)
        punto = punto.reshape(1, -1)
        punto_scaled = self.scaler.transform(punto)
        try:
            pred = self.knn_mahalanobis.predict(punto_scaled)
        except NotFittedError:
            raise Exception("El modelo KNN con distancia de Mahalanobis no está entrenado.")
        return pred[0]

    def distEuclideana1(self, punto: np.ndarray) -> Union[int, float]:
        """
        Clasifica un punto basado en la distancia Euclidiana usando KNN.

        Parámetros:
        - punto: np.ndarray de tres elementos, características del punto a clasificar.

        Retorna:
        - int o float, etiqueta predicha.
        """
        self._validar_punto(punto)
        punto = punto.reshape(1, -1)
        punto_scaled = self.scaler.transform(punto)
        try:
            pred = self.knn_euclidean.predict(punto_scaled)
        except NotFittedError:
            raise Exception("El modelo KNN con distancia Euclidiana no está entrenado.")
        return pred[0]

