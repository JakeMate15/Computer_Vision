import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def generar_puntos():
    try:
        n_puntos = int(input("Ingrese la cantidad de puntos a generar: "))
        rango_min = float(input("Ingrese el valor mínimo del rango: "))
        rango_max = float(input("Ingrese el valor máximo del rango: "))
        if rango_min >= rango_max:
            print("El valor mínimo del rango debe ser menor que el valor máximo.")
            return None, None
        if n_puntos < 1:
            print("La cantidad de puntos debe ser al menos 1.")
            return None, None
    except ValueError:
        print("Por favor, ingrese valores numéricos válidos.")
        return None, None
    puntos = np.random.uniform(low=rango_min, high=rango_max, size=(n_puntos, 2))
    return puntos, n_puntos

def distancia_clusters(puntos, cluster1, cluster2):
    min_dist = np.inf
    for i in cluster1:
        for j in cluster2:
            dist = np.linalg.norm(puntos[i] - puntos[j])
            if dist < min_dist:
                min_dist = dist
    return min_dist

def calcular_matriz_distancias(puntos, clusters):
    n = len(clusters)
    distancias = np.full((n, n), np.inf)
    for i in range(n):
        for j in range(i+1, n):
            dist = distancia_clusters(puntos, clusters[i], clusters[j])
            distancias[i][j] = distancias[j][i] = dist
    return distancias

def clustering_jerarquico(puntos):
    n_puntos = len(puntos)
    clusters = [[i] for i in range(n_puntos)]
    linkage_matrix = []
    paso = 1
    cluster_ids = {i: i for i in range(n_puntos)}
    while len(clusters) > 1:
        print(f"\n--- Paso {paso} ---")
        distancias = calcular_matriz_distancias(puntos, clusters)
        print("Matriz de distancias:")
        print(distancias)
        idx_min = np.unravel_index(np.argmin(distancias), distancias.shape)
        c1, c2 = idx_min
        min_dist = distancias[c1][c2]
        print(f"Clusters a combinar: {clusters[c1]} y {clusters[c2]} con distancia {min_dist:.4f}")
        # Registrar la fusión en la matriz de enlace
        linkage_matrix.append([cluster_ids[clusters[c1][0]], cluster_ids[clusters[c2][0]], min_dist, len(clusters[c1]) + len(clusters[c2])])
        # Actualizar el ID del nuevo cluster
        nuevo_id = n_puntos + paso - 1
        cluster_ids[clusters[c1][0]] = nuevo_id
        cluster_ids[clusters[c2][0]] = nuevo_id
        # Fusionar los clusters
        nuevo_cluster = clusters[c1] + clusters[c2]
        clusters = [clusters[i] for i in range(len(clusters)) if i not in [c1, c2]]
        clusters.append(nuevo_cluster)
        print(f"Clusters después de la combinación: {clusters}")
        paso += 1
    return np.array(linkage_matrix)

def plotear_dendrograma(linkage_matrix, n_puntos):
    plt.figure(figsize=(10, 7))
    dendrogram(linkage_matrix, labels=[str(i) for i in range(n_puntos)])
    plt.title('Dendrograma del Clustering Jerárquico')
    plt.xlabel('Índice de Punto')
    plt.ylabel('Distancia')
    plt.show()

def asignar_clusters(linkage_matrix, n_clusters):
    from scipy.cluster.hierarchy import fcluster
    etiquetas = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
    return etiquetas - 1  # Ajustar etiquetas para que empiecen en 0

def plotear_clusters(puntos, etiquetas, n_clusters):
    plt.figure(figsize=(8, 6))
    plt.scatter(puntos[:,0], puntos[:,1], c=etiquetas, cmap='tab10', edgecolor='k')
    plt.title(f"Clustering con {n_clusters} Clusters")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.show()

def main():
    puntos, n_puntos = generar_puntos()
    if puntos is None:
        return
    print("\nGeneración de puntos completada.")
    print("Puntos generados:")
    for idx, p in enumerate(puntos):
        print(f"Punto {idx}: ({p[0]:.4f}, {p[1]:.4f})")
    plt.figure(figsize=(8, 6))
    plt.scatter(puntos[:,0], puntos[:,1], c='blue', edgecolor='k')
    plt.title("Puntos Originales")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.show()
    linkage_matrix = clustering_jerarquico(puntos)
    plotear_dendrograma(linkage_matrix, n_puntos)
    try:
        n_clusters = int(input("\nIngrese el número deseado de clusters: "))
        if n_clusters < 1 or n_clusters > n_puntos:
            print("El número de clusters debe estar entre 1 y la cantidad de puntos.")
            return
    except ValueError:
        print("Por favor, ingrese un valor entero válido para el número de clusters.")
        return
    etiquetas = asignar_clusters(linkage_matrix, n_clusters)
    plotear_clusters(puntos, etiquetas, n_clusters)

if __name__ == "__main__":
    main()
