import cv2
import numpy as np

class CovarianceMatrixNotInvertibleError(Exception):
    """Excepción lanzada cuando la matriz de covarianza no es invertible."""
    pass

class PuntoNotSetError(Exception):
    """Excepción lanzada cuando el punto no ha sido establecido antes de realizar cálculos."""
    pass

class Clase:
    """
    Clase para manejar datos multidimensionales y calcular la distancia de Mahalanobis y
    la densidad de probabilidad de una distribución normal multivariante.

    Atributos:
        color (str): Color asociado a la clase.
        Punto (np.ndarray): Punto de interés para los cálculos.
        Xv (np.ndarray): Vector de diferencias entre Punto y el centroide.
        Xt (np.ndarray): Transpuesta de Xv.
        S (np.ndarray): Matriz de covarianza.
        sInv (np.ndarray): Inversa de la matriz de covarianza.
        data (np.ndarray): Datos de la clase con dimensiones (n_dimensiones, n_muestras).
        c (np.ndarray): Centroide de los datos.
        n (int): Número de muestras.
        dims (int): Número de dimensiones.

    Métodos:
        __init__: Constructor de la clase.
        preCalc: Calcula matrices necesarias para los cálculos estadísticos.
        mahalanobis: Calcula la distancia de Mahalanobis.
        proB: Calcula la densidad de probabilidad.
        getData: Retorna los datos de la clase.
        getColor: Retorna el color asociado a la clase.
        getPunto: Retorna el punto establecido.
        getCentroid: Retorna el centroide de los datos.
        setData: Establece nuevos datos para la clase.
        setColor: Establece un color para la clase.
        setPunto: Establece el punto de interés y realiza cálculos previos.
    """

    def __init__(self, n=None, c=None, d=None, data=None):
        """
        Inicializa una instancia de la clase Clase.

        Args:
            n (int, opcional): Número de muestras a generar si no se proporcionan datos.
            c (array-like, opcional): Centroide alrededor del cual se generarán los datos.
            d (array-like, opcional): Dispersión para la generación de datos.
            data (array-like, opcional): Datos proporcionados en forma de matriz (n_dimensiones, n_muestras).

        Raises:
            ValueError: Si no se proporcionan datos suficientes para inicializar la clase.
        """
        self.color = ''
        self.Punto = None  # Se establecerá más tarde con setPunto
        self.Xv = None
        self.Xt = None
        self.S = None
        self.sInv = None

        if data is not None:
            # Inicializar con datos proporcionados en forma (n_dimensiones, n_muestras)
            self.data = np.array(data)
            self.dims, self.n = self.data.shape
            self.c = np.mean(self.data, axis=1, keepdims=True)  # Centroide de cada dimensión
        else:
            # Generar datos aleatorios alrededor del centroide c con dispersión d
            if c is None or d is None or n is None:
                raise ValueError("Debe proporcionar 'data' o 'n', 'c' y 'd'.")
            self.n = n
            self.c = np.array(c).reshape(-1, 1)
            self.d = np.array(d).reshape(-1, 1)
            self.dims = self.c.shape[0]
            # Datos aleatorios dentro de [c - d/2, c + d/2]
            low = self.c - self.d / 2
            high = self.c + self.d / 2
            self.data = np.random.uniform(low, high, size=(self.dims, self.n))
            self.c = np.mean(self.data, axis=1, keepdims=True)

    def preCalc(self):
        """
        Calcula las matrices necesarias para los cálculos estadísticos,
        como la matriz de covarianza y su inversa.

        Raises:
            PuntoNotSetError: Si el punto no ha sido establecido.
            CovarianceMatrixNotInvertibleError: Si la matriz de covarianza no es invertible.
        """
        if self.Punto is None:
            raise PuntoNotSetError("Punto no está establecido. Por favor, utilice setPunto antes de llamar a preCalc().")
        # Vector de diferencias entre Punto y centroide
        self.Xv = (self.Punto.reshape(-1, 1) - self.c)  # (dims x 1)
        self.Xt = self.Xv.T  # (1 x dims)
        # Datos centrados
        data_centered = self.data - self.c
        # Matriz de covarianza
        self.S = (data_centered @ data_centered.T) / self.n  # (dims x dims)
        det_S = np.linalg.det(self.S)
        if det_S <= 0:
            raise CovarianceMatrixNotInvertibleError("La matriz de covarianza no es invertible.")
        self.sInv = np.linalg.inv(self.S)

    def mahalanobis(self):
        """
        Calcula la distancia de Mahalanobis entre el punto establecido y el centroide.

        Returns:
            float: Distancia de Mahalanobis.

        Raises:
            CovarianceMatrixNotInvertibleError: Si la matriz de covarianza no es invertible.
        """
        # Cálculo de la distancia de Mahalanobis
        sq = self.Xt @ self.sInv @ self.Xv
        return np.sqrt(sq[0, 0])

    def proB(self):
        """
        Calcula la densidad de probabilidad del punto establecido usando
        la distribución normal multivariante.

        Returns:
            float: Densidad de probabilidad.

        Raises:
            CovarianceMatrixNotInvertibleError: Si la matriz de covarianza no es invertible.
        """
        # Función de densidad de probabilidad de la distribución normal multivariante
        detS = np.linalg.det(self.S)
        if detS <= 0:
            raise CovarianceMatrixNotInvertibleError("La matriz de covarianza no es invertible.")
        d = self.dims
        den = np.sqrt((2 * np.pi) ** d * detS)
        exponent = -0.5 * (self.Xt @ self.sInv @ self.Xv)[0, 0]
        ex = np.exp(exponent)
        return ex / den

    # Getters
    def getData(self):
        """
        Retorna los datos de la clase.

        Returns:
            np.ndarray: Datos de la clase con dimensiones (n_dimensiones, n_muestras).
        """
        return self.data

    def getColor(self):
        """
        Retorna el color asociado a la clase.

        Returns:
            str: Color de la clase.
        """
        return self.color

    def getPunto(self):
        """
        Retorna el punto establecido.

        Returns:
            np.ndarray: Punto de interés.
        """
        return self.Punto

    def getCentroid(self):
        """
        Retorna el centroide de los datos.

        Returns:
            np.ndarray: Centroide con dimensiones (n_dimensiones,).
        """
        return self.c.flatten()

    # Setters
    def setData(self, data):
        """
        Establece nuevos datos para la clase y recalcula el centroide.

        Args:
            data (array-like): Datos nuevos en forma (n_dimensiones, n_muestras).
        """
        self.data = np.array(data)
        self.dims, self.n = self.data.shape
        self.c = np.mean(self.data, axis=1, keepdims=True)

    def setColor(self, color):
        """
        Establece un color para la clase.

        Args:
            color (str): Color a asignar.
        """
        self.color = color

    def setPunto(self, Punto):
        """
        Establece el punto de interés y realiza los cálculos previos necesarios.

        Args:
            Punto (array-like): Punto de interés con dimensiones (n_dimensiones,).
        """
        self.Punto = np.array(Punto)
        self.preCalc()

def getNB(probs):
    """
    Normaliza un array de probabilidades para que sumen 100%.

    Args:
        probs (np.ndarray): Array de probabilidades.

    Modifica:
        probs (np.ndarray): Array de probabilidades normalizadas.
    """
    total = np.sum(probs)
    probs[:] = (probs / total) * 100.0

def analisis(imagen, coordenadas_guardadas, x, y, ancho, alto):
    ruta_imagen = f'static/imagenes/{imagen}'

    img = cv2.imread(ruta_imagen)

    if img is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")

    x = int(x)
    y = int(y)
    ancho = int(ancho)
    alto = int(alto)
    seccionParaAnalizar = img[y:y+alto, x:x+ancho]
    if seccionParaAnalizar.size == 0:
        raise ValueError("La sección para analizar es inválida.")

    (b_punto, g_punto, r_punto) = cv2.split(seccionParaAnalizar)
    punto = np.array([r_punto.mean(), g_punto.mean(), b_punto.mean()])

    resultados = []

    for cord in coordenadas_guardadas:
        xG = int(cord['x'])
        yG = int(cord['y'])
        anchoG = int(cord['ancho'])
        altoG = int(cord['alto'])

        region = img[yG:yG+altoG, xG:xG+anchoG]

        if region.size == 0:
            print(f"La región especificada en {cord} es inválida.")
            continue

        (b, g, r) = cv2.split(region)
        data = np.array([r.flatten(), g.flatten(), b.flatten()])

        clase_obj = Clase(data=data)
        clase_obj.setPunto(punto)

        try:
            mahala_distance = clase_obj.mahalanobis()
            probabilidad = clase_obj.proB()
        except CovarianceMatrixNotInvertibleError as e:
            print(f"Error en la clase con coordenadas {cord}: {e}")
            mahala_distance = np.nan
            probabilidad = np.nan

        centroid = clase_obj.getCentroid()
        euclidean_distance = np.linalg.norm(punto - centroid)

        resultados.append([mahala_distance, euclidean_distance, probabilidad])

    resultados = np.array(resultados)  # (n_clases, 3)

    probs = resultados[:, 2]
    # print(probs)

    if np.max(probs) <= 1e-7:
        resultados[:, 2] = 0
        # print("El máximo de 'probs' es <= 1e-7. Se han establecido todas las probabilidades a 0.")
    else:
        getNB(probs)
        resultados[:, 2] = probs
    return resultados

