import random
from aux import Clasificador

def evaluar(data, k):
    porcentaje = 0.01
    data  = dict(random.sample(data.items(), int(len(data) * porcentaje)))

    X = np.array([info['individuo'] for info in data.values()])
    y = np.array([info['label'] for info in data.values()])

    print("Evaluación con resubstitución:")
    Resust(X, y, k)

    print("\nEvaluación con validación cruzada:")
    validacionCruzada(X, y, k, n_splits=5)

    print("\nEvaluación con Leave-One-Out Cross-Validation:")
    unoFuera(X, y, k)

def evaluacion(y_verdadero, y_predicho):
    etiquetas_unicas = set(y_verdadero) | set(y_predicho)
    etiqueta_a_indice = {etiqueta: idx for idx, etiqueta in enumerate(etiquetas_unicas)}
    n = len(etiquetas_unicas)
    matriz_confusion = [[0] * n for _ in range(n)]

    for verdadero, predicho in zip(y_verdadero, y_predicho):
        matriz_confusion[etiqueta_a_indice[verdadero]][etiqueta_a_indice[predicho]] += 1

    recall_por_clase = []
    r = 0.0
    for i in range(n):
        verdaderos_positivos = matriz_confusion[i][i]
        total_positivos_reales = sum(matriz_confusion[i])
        recall = verdaderos_positivos / total_positivos_reales if total_positivos_reales > 0 else 0
        recall_por_clase.append(recall)
        r += recall

    return matriz_confusion, recall_por_clase, r / n

def Resust(X, y, k):
    c = Clasificador(X, y, k)
    y_pred_prob = c.maxProb(X)
    y_pred_maha = c.distMahalanobis(X)
    y_pred_eu = c.distEuclideana(X)

    evProb = evaluacion(y, y_pred_prob)
    evMaha = evaluacion(y, y_pred_maha)
    evEuc = evaluacion(y, y_pred_eu)

    print(evProb)
    print(evMaha)
    print(evEuc)


def validacionCruzada(X, y, k, n_splits=5):
    """
    Realiza validación cruzada k-fold manualmente en los datos X e y.

    Parámetros:
    - X: np.ndarray, matriz de características.
    - y: np.ndarray, vector de etiquetas.
    - k: int, número de vecinos a considerar en KNN.
    - n_splits: int, número de folds en la validación cruzada (por defecto 5).

    Retorna:
    - Nada. Imprime las métricas de evaluación.
    """
    # Establecer una semilla para reproducibilidad
    np.random.seed(42)

    # Mezclar los datos aleatoriamente
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    X_shuffled = X[indices]
    y_shuffled = y[indices]

    # Calcular el tamaño de cada fold
    fold_sizes = np.full(n_splits, len(X) // n_splits, dtype=int)
    fold_sizes[:len(X) % n_splits] += 1  # Distribuir el resto

    # Crear los índices para cada fold
    current = 0
    folds = []
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size
        folds.append((start, stop))
        current = stop

    # Listas para almacenar las métricas
    recalls_prob = []
    recalls_maha = []
    recalls_eu = []

    for fold_num, (start, stop) in enumerate(folds):
        # Índices de prueba y entrenamiento
        test_indices = np.arange(start, stop)
        train_indices = np.concatenate([np.arange(0, start), np.arange(stop, len(X))])

        # Dividir los datos
        X_train, X_test = X_shuffled[train_indices], X_shuffled[test_indices]
        y_train, y_test = y_shuffled[train_indices], y_shuffled[test_indices]

        # Entrenar el clasificador con los datos de entrenamiento
        c = Clasificador(X_train, y_train, k)

        # Predecir las etiquetas para los datos de prueba
        y_pred_prob = c.maxProb(X_test)
        y_pred_maha = c.distMahalanobis(X_test)
        y_pred_eu = c.distEuclideana(X_test)

        # Evaluar el rendimiento utilizando la función 'evaluacion'
        evProb = evaluacion(y_test, y_pred_prob)
        evMaha = evaluacion(y_test, y_pred_maha)
        evEuc = evaluacion(y_test, y_pred_eu)

        # Extraer el recall promedio
        recall_prob = evProb[2]
        recall_maha = evMaha[2]
        recall_eu = evEuc[2]

        # Almacenar los recalls
        recalls_prob.append(recall_prob)
        recalls_maha.append(recall_maha)
        recalls_eu.append(recall_eu)

        # Opcional: imprimir métricas por fold
        print(f"Fold {fold_num + 1}/{n_splits}")
        print(f"  Recall (Máxima Probabilidad): {recall_prob:.4f}")
        print(f"  Recall (Distancia Mahalanobis): {recall_maha:.4f}")
        print(f"  Recall (Distancia Euclidiana): {recall_eu:.4f}")

    # Calcular el recall promedio en todos los folds
    mean_recall_prob = np.mean(recalls_prob)
    mean_recall_maha = np.mean(recalls_maha)
    mean_recall_eu = np.mean(recalls_eu)

    print("\nResultados finales:")
    print(f"Recall promedio (Máxima Probabilidad): {mean_recall_prob:.4f}")
    print(f"Recall promedio (Distancia Mahalanobis): {mean_recall_maha:.4f}")
    print(f"Recall promedio (Distancia Euclidiana): {mean_recall_eu:.4f}")

import numpy as np

def unoFuera(X, y, k):
    """
    Realiza validación cruzada Leave-One-Out manualmente en los datos X e y.

    Parámetros:
    - X: np.ndarray, matriz de características.
    - y: np.ndarray, vector de etiquetas.
    - k: int, número de vecinos a considerar en KNN.

    Retorna:
    - Nada. Imprime las métricas de evaluación.
    """
    n_samples = len(X)
    # Listas para almacenar las etiquetas verdaderas y predichas
    y_true = []
    y_pred_prob = []
    y_pred_maha = []
    y_pred_eu = []

    for i in range(n_samples):
        # Separar la muestra i para prueba
        X_test = X[i].reshape(1, -1)
        y_test = y[i]

        # Utilizar el resto de las muestras para entrenamiento
        X_train = np.delete(X, i, axis=0)
        y_train = np.delete(y, i)

        # Entrenar el clasificador con los datos de entrenamiento
        c = Clasificador(X_train, y_train, k)

        # Predecir la etiqueta para el dato de prueba utilizando los tres métodos
        pred_prob = c.maxProb1(X_test[0])
        pred_maha = c.distMahalanobis1(X_test[0])
        pred_eu = c.distEuclideana1(X_test[0])

        # Almacenar las etiquetas verdaderas y las predicciones
        y_true.append(y_test)
        y_pred_prob.append(pred_prob)
        y_pred_maha.append(pred_maha)
        y_pred_eu.append(pred_eu)

        if (i + 1) % 100 == 0 or (i + 1) == n_samples:
            print(f"Procesado {i + 1}/{n_samples} muestras...")

    # Convertir las listas a arrays numpy
    y_true = np.array(y_true)
    y_pred_prob = np.array(y_pred_prob)
    y_pred_maha = np.array(y_pred_maha)
    y_pred_eu = np.array(y_pred_eu)

    # Evaluar el rendimiento utilizando la función 'evaluacion'
    evProb = evaluacion(y_true, y_pred_prob)
    evMaha = evaluacion(y_true, y_pred_maha)
    evEuc = evaluacion(y_true, y_pred_eu)

    # Imprimir los resultados
    print("\nResultados Leave-One-Out Cross-Validation:")
    print(f"Recall promedio (Máxima Probabilidad): {evProb[2]:.4f}")
    print(f"Recall promedio (Distancia Mahalanobis): {evMaha[2]:.4f}")
    print(f"Recall promedio (Distancia Euclidiana): {evEuc[2]:.4f}")
