import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

puntos = np.array([
    [1.0, 1.25],
    [4.25, 2.75],
    [7.0, 1.5],
    [-10, -10],
    [10, 10],
    [-10, 10],
    [10, -10]
])

c1 = np.array([[0, 1, 0, 3], [0, 2, 3, 0]])
c2 = np.array([[4, 4, 4, 5], [0, 3, 2, 6]])
c3 = np.array([[6, 7, 7, 8], [0, 1, 3, 2]])
v = np.array([3, -4])

vor = Voronoi(puntos)

fig, ax = plt.subplots(figsize=(12, 10))
voronoi_plot_2d(vor, ax=ax)

ax.plot(puntos[:, 0], puntos[:, 1], 'o', color='red', markersize=8, label='Puntos Voronoi')

for i, (x, y) in enumerate(puntos):
    ax.text(x, y, f'P{i+1}', fontsize=12, ha='right', color='red')

ax.plot(c1[0], c1[1], 'o', color='green', markersize=8, label='c1')
ax.plot(c2[0], c2[1], 'o', color='orange', markersize=8, label='c2')
ax.plot(c3[0], c3[1], 'o', color='purple', markersize=8, label='c3')
ax.plot(v[0], v[1], 'o', color='black', markersize=10, label='Punto v')

for i, (x, y) in enumerate(zip(c1[0], c1[1])):
    ax.text(x, y, f'c1_{i+1}', fontsize=12, ha='right', color='green')

for i, (x, y) in enumerate(zip(c2[0], c2[1])):
    ax.text(x, y, f'c2_{i+1}', fontsize=12, ha='right', color='orange')

for i, (x, y) in enumerate(zip(c3[0], c3[1])):
    ax.text(x, y, f'c3_{i+1}', fontsize=12, ha='right', color='purple')

ax.text(v[0], v[1], 'v', fontsize=12, ha='right', color='black')

min_x = min(vor.vertices[:, 0]) - 1
max_x = max(vor.vertices[:, 0]) + 1
min_y = min(vor.vertices[:, 1]) - 1
max_y = max(vor.vertices[:, 1]) + 1

ax.set_xlim([min_x, max_x])
ax.set_ylim([min_y, max_y])
ax.set_aspect('equal')
plt.title('Diagrama de Voronoi con Puntos Adicionales y Punto v')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)
plt.show()
