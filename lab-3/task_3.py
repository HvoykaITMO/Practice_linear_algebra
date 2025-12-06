import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Patch
from util import transform_points
from matrix import translate_matrix, scale_matrix
from pprint import pprint


def draw_shape(ax, vertices, faces, color):
    """Рисует 3D фигуру"""
    vertices_3d = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices_3d[faces], 
                                         facecolors=color,
                                         edgecolors='k', 
                                         linewidths=0.2))


def main(vertices_original, vertices_transformed, faces_cube, title="Преобразование", m=None):
    """Показывает оба куба на одной сцене"""
    if m is None:
        m = max(np.max(np.abs(vertices_original)), 
                np.max(np.abs(vertices_transformed)))
    
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
    tx, ty, tz = 0, 0, 3
    t1 = translate_matrix(tx, ty, tz)
    print("t1:")
    pprint(t1)
    translated_vertices = transform_points(vertices_cube, t1)
    m = np.max(np.abs(translated_vertices)) + 1
    
    main(
        vertices_cube, 
        translated_vertices, 
        faces_cube, 
        title=f"Трансляция куба на ({tx}, {ty}, {tz})",
        m=m
    )

    # ========== Second matrix ==========
    tx, ty, tz = 0, 2, 0
    t2 = translate_matrix(tx, ty, tz)
    print("t2:")
    pprint(t2)
    translated_vertices = transform_points(vertices_cube, t2)
    m = np.max(np.abs(translated_vertices)) + 1
    
    main(
        vertices_cube, 
        translated_vertices, 
        faces_cube, 
        title=f"Трансляция куба на ({tx}, {ty}, {tz})",
        m=m
    )

    # ========== Third matrix (composition) ==========
    t3 = t1 @ t2
    print("t3 = t1 @ t2:")
    pprint(t3)
    translated_vertices = transform_points(vertices_cube, t3)
    m = np.max(np.abs(translated_vertices)) + 1
    
    main(
        vertices_cube, 
        translated_vertices, 
        faces_cube, 
        title=f"Трансляция куба (композиция)",
        m=m
    )

    # ========== TS ==========
    s = scale_matrix(1, 2, 1)
    ts = t1 @ s
    print("TS = t1 @ s:")
    pprint(ts)
    translated_vertices = transform_points(vertices_cube, ts)
    m = np.max(np.abs(translated_vertices)) + 1
    
    main(
        vertices_cube, 
        translated_vertices, 
        faces_cube, 
        title=f"Трансляция куба (TS)",
        m=m
    )

    # ========== ST ==========
    st = s @ t1
    print("ST = s @ t1:")
    pprint(st)
    translated_vertices = transform_points(vertices_cube, st)
    m = np.max(np.abs(translated_vertices)) + 1
    
    main(
        vertices_cube, 
        translated_vertices, 
        faces_cube, 
        title=f"Трансляция куба (ST)",
        m=m
    )
