import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from util import transform_points
from matrix import scale_matrix
from pprint import pprint


def draw_shape(ax, vertices, faces, color):
    """Рисует 3D фигуру"""
    vertices_3d = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices_3d[faces], 
                                         facecolors=color,
                                         edgecolors='k', 
                                         linewidths=0.2))


def main(vertices_original, vertices_transformed, faces_cube, title="Преобразование", m=None):
    """Показывает два графика: до и после преобразования"""
    if m is None:
        m = max(np.max(np.abs(vertices_original)), 
                np.max(np.abs(vertices_transformed)))
    
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


if __name__ == '__main__':
    vertices_cube = np.array([
        [-1,  1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1,  1],
        [-1, -1, -1, -1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1]
    ], dtype=float)

    faces_cube = np.array([
        [0, 1, 5, 4],
        [1, 2, 6, 5],
        [2, 3, 7, 6],
        [3, 0, 4, 7],
        [0, 1, 2, 3],
        [4, 5, 6, 7]
    ])
    
    # ========== First matrix ==========
    sx, sy, sz = 1, 3, 1
    s1 = scale_matrix(sx, sy, sz)
    print("s1:")
    pprint(s1)
    new_vertices = transform_points(vertices_cube, s1)
    
    main(
        vertices_cube, 
        new_vertices, 
        faces_cube, 
        title=f"Масштабирование: ({sx}, {sy}, {sz})"
    )

    # ========== Second matrix ==========
    sx, sy, sz = 2, 1, 2
    s2 = scale_matrix(sx, sy, sz)
    print("s2:")
    pprint(s2)
    new_vertices = transform_points(vertices_cube, s2)
    
    main(
        vertices_cube, 
        new_vertices, 
        faces_cube, 
        title=f"Масштабирование: ({sx}, {sy}, {sz})"
    )

    # ========== Third matrix (composition) ==========
    s3 = s1 @ s2
    print("s3 = s1 @ s2:")
    pprint(s3)
    new_vertices = transform_points(vertices_cube, s3)
    
    main(
        vertices_cube, 
        new_vertices, 
        faces_cube, 
        title=f"Масштабирование: (композиция)"
    )
