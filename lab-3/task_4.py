import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from util import transform_points
from matrix import rotation_matrix
from pprint import pprint


def draw_shape(ax, vertices, faces, color):
    """Рисует 3D фигуру"""
    vertices_3d = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices_3d[faces], 
                                         facecolors=color,
                                         edgecolors='k', 
                                         linewidths=0.2))


def draw_axis_vector(ax, v, color='green', label='Ось вращения'):
    """Рисует одну ось как толстую линию с шариком в конце"""
    v_norm = v / np.linalg.norm(v)
    scale = 2.0
    v_scaled = v_norm * scale
    
    # Линия через центр
    ax.plot([-v_scaled[0], v_scaled[0]], 
            [-v_scaled[1], v_scaled[1]], 
            [-v_scaled[2], v_scaled[2]],
            color=color, 
            linewidth=4,
            label=label)
    
    # Шарик на конце
    ax.scatter([v_scaled[0]], [v_scaled[1]], [v_scaled[2]],
              color=color, s=100, marker='o', edgecolors='black', linewidths=2)


def draw_axis_vectors(ax, vectors_list, colors=None, labels=None):
    """Рисует несколько осей вращения разными цветами"""
    if colors is None:
        colors = ['green', 'red', 'blue', 'orange']
    if labels is None:
        labels = [f'Ось {i+1}' for i in range(len(vectors_list))]
    
    for v, color, label in zip(vectors_list, colors, labels):
        v_norm = v / np.linalg.norm(v)
        scale = 2.0
        v_scaled = v_norm * scale
        
        ax.plot([-v_scaled[0], v_scaled[0]], 
                [-v_scaled[1], v_scaled[1]], 
                [-v_scaled[2], v_scaled[2]],
                color=color, 
                linewidth=4,
                label=label)
        
        ax.scatter([v_scaled[0]], [v_scaled[1]], [v_scaled[2]],
                  color=color, s=100, marker='o', edgecolors='black', linewidths=2)


def main(vertices_original, vertices_transformed, faces_cube, 
         axis_vector=None, axis_vectors=None, colors=None, labels=None,
         title="Преобразование", m=None):
    """Показывает два графика: до и после преобразования"""
    if m is None:
        m_vertices = max(np.max(np.abs(vertices_original)), 
                        np.max(np.abs(vertices_transformed)))
        m = m_vertices
    
    # Если есть вектора осей, увеличиваем масштаб
    if axis_vector is not None or axis_vectors is not None:
        axis_scale = 2.0
        m = max(m, axis_scale)
    
    fig = plt.figure(figsize=(14, 6))
    
    # Левый график - оригинал
    ax1 = fig.add_subplot(1, 2, 1, projection='3d', proj_type='ortho')
    draw_shape(ax1, vertices_original, faces_cube, 'blue')
    
    if axis_vector is not None:
        draw_axis_vector(ax1, axis_vector, color='green', label='Ось вращения')
    elif axis_vectors is not None:
        draw_axis_vectors(ax1, axis_vectors, colors, labels)
    
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
    if axis_vector is not None or axis_vectors is not None:
        ax1.legend(fontsize=8)
    
    # Правый график - результат преобразования
    ax2 = fig.add_subplot(1, 2, 2, projection='3d', proj_type='ortho')
    draw_shape(ax2, vertices_transformed, faces_cube, 'red')
    
    if axis_vector is not None:
        draw_axis_vector(ax2, axis_vector, color='green', label='Ось вращения')
    elif axis_vectors is not None:
        draw_axis_vectors(ax2, axis_vectors, colors, labels)
    
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
    if axis_vector is not None or axis_vectors is not None:
        ax2.legend(fontsize=8)
    
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
    
    # ========== Первый поворот ==========
    v1 = np.array([1.0, 1.0, 0.0])
    theta1 = np.pi/4
    R1 = rotation_matrix(v1, theta1)
    
    print("=" * 60)
    print(f"ПЕРВЫЙ ПОВОРОТ: v1 = {v1}, θ1 = π/4")
    print("=" * 60)
    print("Матрица R1:")
    pprint(R1)
    
    new_vertices_1 = transform_points(vertices_cube, R1)
    
    main(
        vertices_cube, 
        new_vertices_1, 
        faces_cube, 
        axis_vector=v1,
        title=f"Поворот 1 (вектор v: ({v1[0]}, {v1[1]}, {v1[2]}), θ = π/4)"
    )

    # ========== Второй поворот ==========
    v2 = np.array([0.0, 2.0, 1.0])
    theta2 = np.pi/3
    R2 = rotation_matrix(v2, theta2)
    
    print("\n" + "=" * 60)
    print(f"ВТОРОЙ ПОВОРОТ: v2 = {v2}, θ2 = π/3")
    print("=" * 60)
    print("Матрица R2:")
    pprint(R2)
    
    new_vertices_2 = transform_points(vertices_cube, R2)
    
    main(
        vertices_cube, 
        new_vertices_2, 
        faces_cube, 
        axis_vector=v2,
        title=f"Поворот 2 (вектор v: ({v2[0]}, {v2[1]}, {v2[2]}), θ = π/3)"
    )

    # ========== Объединение R1 @ R2 (сначала R1, потом R2) ==========
    R12 = R2 @ R1
    
    print("\n" + "=" * 60)
    print("КОМПОЗИЦИЯ: R12 = R2 @ R1 (сначала R1, потом R2)")
    print("=" * 60)
    print("Матрица R12:")
    pprint(R12)
    
    new_vertices_12 = transform_points(vertices_cube, R12)
    
    main(
        vertices_cube, 
        new_vertices_12, 
        faces_cube, 
        axis_vectors=[v1, v2],
        colors=['green', 'red'],
        labels=[f'v1 = {v1}', f'v2 = {v2}'],
        title=f"Композиция: R12 = R2 @ R1 (оси обеих поворотов)"
    )

    # ========== Объединение R2 @ R1 (сначала R2, потом R1) ==========
    R21 = R1 @ R2
    
    print("\n" + "=" * 60)
    print("КОМПОЗИЦИЯ: R21 = R1 @ R2 (сначала R2, потом R1)")
    print("=" * 60)
    print("Матрица R21:")
    pprint(R21)
    
    new_vertices_21 = transform_points(vertices_cube, R21)
    
    main(
        vertices_cube, 
        new_vertices_21, 
        faces_cube, 
        axis_vectors=[v2, v1],
        colors=['red', 'green'],
        labels=[f'v2 = {v2}', f'v1 = {v1}'],
        title=f"Композиция: R21 = R1 @ R2 (оси обеих поворотов)"
    )
