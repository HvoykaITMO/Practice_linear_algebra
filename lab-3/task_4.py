import numpy as np
import matplotlib.pyplot as plt
from sympy import Matrix
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from util import *


def draw_shape(ax, vertices, faces, color):
    vertices = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices[faces], facecolors=color
        , edgecolors='k', linewidths=0.2))


def main(vertices_original, vertices_transformed, faces_cube, title="Преобразование", m=None):
    if m is None:
        m = max(np.max(np.abs(vertices_original)), np.max(np.abs(vertices_transformed)))
    
    fig = plt.figure(figsize=(14, 6))
    
    # Левый график - оригинал
    ax1 = fig.add_subplot(1, 2, 1, projection='3d', proj_type='ortho')
    draw_shape(ax1, vertices_original, faces_cube, 'blue')
    
    ax1.set_box_aspect([1, 1, 1])
    ax1.set_xlim(-m, m)
    ax1.set_ylim(-m, m)
    ax1.set_zlim(-m, m)
    ax1.view_init(azim=-37.5, elev=30)
    ax1.set_xticks(np.linspace(-m, m, 5))
    ax1.set_yticks(np.linspace(-m, m, 5))
    ax1.set_zticks(np.linspace(-m, m, 5))
    ax1.set_title("До преобразования", fontsize=12, fontweight='bold')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')
    
    # Правый график - результат преобразования
    ax2 = fig.add_subplot(1, 2, 2, projection='3d', proj_type='ortho')
    draw_shape(ax2, vertices_transformed, faces_cube, 'red')
    
    ax2.set_box_aspect([1, 1, 1])
    ax2.set_xlim(-m, m)
    ax2.set_ylim(-m, m)
    ax2.set_zlim(-m, m)
    ax2.view_init(azim=-37.5, elev=30)
    ax2.set_xticks(np.linspace(-m, m, 5))
    ax2.set_yticks(np.linspace(-m, m, 5))
    ax2.set_zticks(np.linspace(-m, m, 5))
    ax2.set_title("После преобразования", fontsize=12, fontweight='bold')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_zlabel('Z')
    
    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def rotate_x(a):
    return Matrix([
        [1, 0,       0,      0],
        [0, np.cos(a), -np.sin(a), 0],
        [0, np.sin(a),  np.cos(a), 0],
        [0, 0,       0,      1],
    ])

def rotate_y(a):
    return Matrix([
        [ np.cos(a), 0, np.sin(a), 0],
        [ 0,      1, 0,      0],
        [-np.sin(a), 0, np.cos(a), 0],
        [ 0,      0, 0,      1],
    ])
    
def rotate_z(a):
    return Matrix([
        [np.cos(a), -np.sin(a), 0, 0],
        [np.sin(a),  np.cos(a), 0, 0],
        [0,       0,      1, 0],
        [0,       0,      0, 1],
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
    
    sx, sy, sz = 1, 3, 1
    new_vertices = transform_points(vertices_cube, rotate_x(90))
    

    main(
        vertices_cube, 
        new_vertices, 
        faces_cube, 
        title=f"Поворот: ({sx}, {sy}, {sz})"
    )
