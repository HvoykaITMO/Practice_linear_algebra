import numpy as np
import matplotlib.pyplot as plt
from sympy import Matrix
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch
from util import *


def draw_shape(ax, vertices, faces, color):
    vertices = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices[faces], facecolors=color
        , edgecolors='k', linewidths=0.2))


def main_compare_same_scene(vertices_original, vertices_transformed, faces_cube, title="Преобразование", m=None):
    if m is None:
        m = max(np.max(np.abs(vertices_original)), np.max(np.abs(vertices_transformed)))
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d', proj_type='ortho')
    
    # Оба куба на одной сцене
    draw_shape(ax, vertices_original, faces_cube, 'blue')
    draw_shape(ax, vertices_transformed, faces_cube, 'red')
    
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlim(-m, m)
    ax.set_ylim(-m, m)
    ax.set_zlim(-m, m)
    ax.view_init(azim=-37.5, elev=30)
    ax.set_xticks(np.linspace(-m, m, 5))
    ax.set_yticks(np.linspace(-m, m, 5))
    ax.set_zticks(np.linspace(-m, m, 5))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Легенда
    legend_elements = [
        Patch(facecolor='blue', edgecolor='k', label='До преобразования'),
        Patch(facecolor='red', edgecolor='k', label='После преобразования')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def translate_matrix(tx, ty, tz):
    return Matrix([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],
    ])


if __name__ == '__main__':
    vertices_cube = np.array([
        [-1,  1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1,  1],
        [-1, -1, -1, -1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1]
    ])

    faces_cube = np.array([
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7],
        [0, 1, 2, 3],
        [4, 5, 6, 7]
    ])
    
    tx, ty, tz = 0, 0, 3
    translated_vertices = transform_points(vertices_cube, translate_matrix(tx, ty, tz))
    m = np.max(np.abs(translated_vertices)) + 1  # небольшой запас
    
    main_compare_same_scene(
        vertices_cube, 
        translated_vertices, 
        faces_cube, 
        title=f"Трансляция куба на ({tx}, {ty}, {tz})",
        m=m
    )
