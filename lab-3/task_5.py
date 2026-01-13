import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from util import transform_points
from matrix import rotation_matrix, rotation_around_point
from pprint import pprint


def draw_shape(ax, vertices, faces, color):
    """Рисует 3D фигуру"""
    vertices_3d = (vertices[:3, :] / vertices[3, :]).T
    ax.add_collection3d(Poly3DCollection(vertices_3d[faces], 
                                         facecolors=color,
                                         edgecolors='k', 
                                         linewidths=0.2))


def draw_axis_vector(ax, v, M=None, color='green', label='Ось вращения'):
    """Рисует ось вращения"""
    v_norm = v / np.linalg.norm(v)
    scale = 2.0
    v_scaled = v_norm * scale
    
    if M is None:
        # Ось через начало координат
        ax.plot([-v_scaled[0], v_scaled[0]], 
                [-v_scaled[1], v_scaled[1]], 
                [-v_scaled[2], v_scaled[2]],
                color=color, 
                linewidth=4,
                label=label)
        ax.scatter([v_scaled[0]], [v_scaled[1]], [v_scaled[2]],
                  color=color, s=100, marker='o', edgecolors='black', linewidths=2)
    else:
        # Ось через точку M
        M3 = M[:3] / M[3] if len(M) == 4 else M
        start = M3 - v_scaled
        end = M3 + v_scaled
        
        ax.plot([start[0], end[0]], 
                [start[1], end[1]], 
                [start[2], end[2]],
                color=color, 
                linewidth=4,
                label=label)
        
        # Точка M
        ax.scatter([M3[0]], [M3[1]], [M3[2]],
                  color=color, s=150, marker='*', edgecolors='black', linewidths=2)


def main(vertices_original, vertices_transformed, faces_cube, 
         axis_vector=None, point_M=None,
         title="Преобразование", m=None):
    """Показывает два графика: до и после преобразования"""
    if m is None:
        m_vertices = max(np.max(np.abs(vertices_original)), 
                        np.max(np.abs(vertices_transformed)))
        m = m_vertices
    
    if axis_vector is not None:
        axis_scale = 2.5
        m = max(m, axis_scale)
    
    fig = plt.figure(figsize=(14, 6))
    
    # Левый график - оригинал
    ax1 = fig.add_subplot(1, 2, 1, projection='3d', proj_type='ortho')
    draw_shape(ax1, vertices_original, faces_cube, 'blue')
    
    if axis_vector is not None:
        draw_axis_vector(ax1, axis_vector, M=point_M, color='green', label='Ось вращения')
    
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
    if axis_vector is not None:
        ax1.legend(fontsize=8)
    
    # Правый график - результат преобразования
    ax2 = fig.add_subplot(1, 2, 2, projection='3d', proj_type='ortho')
    draw_shape(ax2, vertices_transformed, faces_cube, 'red')
    
    if axis_vector is not None:
        draw_axis_vector(ax2, axis_vector, M=point_M, color='green', label='Ось вращения')
    
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
    if axis_vector is not None:
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
    
    # ========== Поворот вокруг вершины ==========
    # Выбираем вершину куба (индекс 0 = вершина [-1, -1, -1])
    vertex_index = 0
    M = vertices_cube[:, vertex_index]  # однородные координаты
    M3 = M[:3] / M[3]  # (x, y, z)
    
    v = np.array([1.0, 1.0, 1.0])  # направление оси (диагональ куба!)
    theta = np.pi / 3  # 60 градусов
    
    print("=" * 60)
    print(f"ПОВОРОТ ВОКРУГ ВЕРШИНЫ M = {M3}")
    print(f"Направление оси: v = {v}")
    print(f"Угол поворота: θ = π/3 (60°)")
    print("=" * 60)
    
    # Матрица поворота
    R_M = rotation_around_point(v, theta, M)
    
    print("Матрица поворота R_M = T(M) @ R_v(θ) @ T(-M):")
    pprint(R_M)
    
    # Применяем к кубу
    new_vertices = transform_points(vertices_cube, R_M)
    
    main(
        vertices_cube, 
        new_vertices, 
        faces_cube, 
        axis_vector=v,
        point_M=M,
        title=f"Поворот вокруг вершины M = {M3} на угол π/3"
    )
    
    # ========== Второй пример: другая вершина ==========
    vertex_index_2 = 7
    M2 = vertices_cube[:, vertex_index_2]
    M2_3d = M2[:3] / M2[3]
    
    v2 = np.array([1.0, 0.0, 0.0])  # ось X
    theta2 = np.pi / 4  # 45 градусов
    
    print("\n" + "=" * 60)
    print(f"ПОВОРОТ ВОКРУГ ВЕРШИНЫ M2 = {M2_3d}")
    print(f"Направление оси: v2 = {v2}")
    print(f"Угол поворота: θ = π/4 (45°)")
    print("=" * 60)
    
    R_M2 = rotation_around_point(v2, theta2, M2)
    
    print("Матрица поворота R_M2:")
    pprint(R_M2)
    
    new_vertices_2 = transform_points(vertices_cube, R_M2)
    
    main(
        vertices_cube, 
        new_vertices_2, 
        faces_cube, 
        axis_vector=v2,
        point_M=M2,
        title=f"Поворот вокруг вершины M2 = {M2_3d} на угол π/4"
    )
