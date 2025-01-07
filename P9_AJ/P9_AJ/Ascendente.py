import random
import math
import matplotlib.pyplot as plt

# Función para generar puntos aleatorios
def generar_puntos():
    try:
        n_puntos = int(input("Ingrese la cantidad de puntos a generar: "))
        rango_min = float(input("Ingrese el valor mínimo del rango: "))
        rango_max = float(input("Ingrese el valor máximo del rango: "))
        if rango_min >= rango_max:
            print("El valor mínimo del rango debe ser menor que el valor máximo.")
            return None, None
    except ValueError:
        print("Por favor, ingrese valores numéricos válidos.")
        return None, None

    # Generar puntos aleatorios dentro del rango especificado
    puntos = []
    for _ in range(n_puntos):
        x = random.uniform(rango_min, rango_max)
        y = random.uniform(rango_min, rango_max)
        puntos.append((x, y))
    return puntos, n_puntos

# Función para calcular la distancia Euclidiana entre dos puntos
def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Función para inicializar cada punto como un cluster separado
def inicializar_clusters(puntos):
    clusters = []
    for punto in puntos:
        clusters.append([punto])
    return clusters

# Función para encontrar los dos clusters más cercanos
def encontrar_clusters_mas_cercanos(clusters, metodo='average'):
    min_dist = float('inf')
    pair = (None, None)

    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            dist = calcular_distancia(clusters[i], clusters[j], metodo)
            if dist < min_dist:
                min_dist = dist
                pair = (i, j)
    return pair, min_dist

# Función para calcular la distancia entre dos clusters según el método de enlace promedio
def calcular_distancia(cluster1, cluster2, metodo):
    if metodo == 'average':
        # Enlace promedio: distancia promedio entre todos los pares de puntos
        total = 0
        count = 0
        for p1 in cluster1:
            for p2 in cluster2:
                total += distancia(p1, p2)
                count += 1
        return total / count
    else:
        # Por defecto, enlace promedio
        total = 0
        count = 0
        for p1 in cluster1:
            for p2 in cluster2:
                total += distancia(p1, p2)
                count += 1
        return total / count

# Función principal del algoritmo de clustering ascendente jerárquico
def clustering_ascendente(puntos, n_clusters=2, metodo='average'):
    clusters = inicializar_clusters(puntos)
    historial = []  # Para almacenar el historial de fusiones
    cluster_indices = {i: [i] for i in range(len(clusters))}  # Para rastrear índices originales

    while len(clusters) > n_clusters:
        (i, j), dist = encontrar_clusters_mas_cercanos(clusters, metodo)
        # Fusionar los clusters i y j
        clusters[i] = clusters[i] + clusters[j]
        del clusters[j]
        historial.append((i, j, dist))
    return clusters, historial

# Función para plotear los puntos generados
def plot_puntos(puntos):
    x = [p[0] for p in puntos]
    y = [p[1] for p in puntos]
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, c='blue', edgecolor='k', alpha=0.7)
    plt.title("Puntos Generados Aleatoriamente")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True)
    plt.show()

# Función para plotear los clusters
def plot_clusters(clusters):
    plt.figure(figsize=(8, 6))
    plt.title(f"Clustering Ascendente Jerárquico con {len(clusters)} Clusters (Enlace Promedio)")
    cmap = plt.colormaps['tab10']  # Actualización para evitar la advertencia de deprecación
    for idx, cluster in enumerate(clusters):
        x = [p[0] for p in cluster]
        y = [p[1] for p in cluster]
        color = cmap(idx % 10)
        plt.scatter(x, y, color=color, edgecolor='k', alpha=0.7, label=f'Cluster {idx+1}')
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.grid(True)
    plt.show()

# Función para plotear un dendrograma básico
def plot_dendrogram(historial, n_puntos):
    # Asignar una posición a cada punto inicial
    posiciones = {i: i for i in range(n_puntos)}
    current_pos = n_puntos
    plt.figure(figsize=(10, 7))
    plt.title("Dendrograma del Clustering Ascendente Jerárquico (Enlace Promedio)")
    plt.xlabel("Índice de Punto de Datos")
    plt.ylabel("Distancia de Fusión")

    for merge in historial:
        i, j, dist = merge
        x1 = posiciones[i]
        x2 = posiciones[j]
        y = dist

        # Dibujar líneas verticales
        plt.plot([x1, x1], [0, y], c='b')
        plt.plot([x2, x2], [0, y], c='b')

        # Dibujar línea horizontal
        plt.plot([x1, x2], [y, y], c='b')

        # Asignar la posición del nuevo cluster
        posiciones[current_pos] = (x1 + x2) / 2
        current_pos += 1

    plt.show()

# Función principal
def main():
    puntos, n_puntos = generar_puntos()
    if puntos is None:
        return

    print("\nGeneración de puntos completada.")
    print("Puntos generados:")
    for punto in puntos:
        print(punto)

    # Mostrar gráfica de los puntos generados antes del clustering
    plot_puntos(puntos)

    # Método de enlace fijo a 'average'
    metodo = 'average'

    # Preguntar al usuario por el número de clusters deseado
    try:
        n_clusters = int(input("\nIngrese el número deseado de clusters: "))
        if n_clusters < 1 or n_clusters > n_puntos:
            print("El número de clusters debe estar entre 1 y la cantidad de puntos.")
            return
    except ValueError:
        print("Por favor, ingrese un valor entero válido para el número de clusters.")
        return

    # Realizar el clustering
    clusters, historial = clustering_ascendente(puntos, n_clusters, metodo)

    # Mostrar los clusters resultantes
    print(f"\nClusters formados ({n_clusters}):")
    for idx, cluster in enumerate(clusters):
        print(f"\nCluster {idx+1}:")
        for punto in cluster:
            print(punto)

    # Plotear los clusters
    plot_clusters(clusters)

    # Plotear el dendrograma
    plot_dendrogram(historial, n_puntos)

if __name__ == "__main__":
    main()
