import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from pprint import pprint
from matrix import (
    scale_matrix, 
    translate_matrix, 
    rotation_matrix,
    view_matrix
)


def draw_shape(ax, vertices, faces, color, alpha=0.7):
    """
    Рисует 3D фигуру на осях matplotlib.
    
    ax: объект 3D axes (fig.add_subplot(..., projection='3d'))
    vertices: (4, N) матрица в однородных координатах
    faces: массив индексов вершин, образующих грани
    color: цвет фигуры (строка типа 'blue', 'red')
    alpha: прозрачность (0-1)
    """
    # Конвертируем однородные координаты (4, N) в обычные (N, 3)
    # Делим на 4-ю координату (w), чтобы получить декартовы координаты
    vertices_3d = (vertices[:3, :] / vertices[3, :]).T
    
    # add_collection3d() добавляет в axes коллекцию полигонов (граней куба)
    # Poly3DCollection создает грани по индексам вершин из faces
    ax.add_collection3d(Poly3DCollection(
        vertices_3d[faces],          # каждая грань - набор вершин по индексам
        facecolors=color,            # цвет заливки грани
        edgecolors='k',              # черный контур грани
        linewidths=0.5,              # толщина линии контура
        alpha=alpha                  # прозрачность
    ))


def draw_camera_frustum(ax, camera_pos, camera_forward, color='red'):
    """
    Рисует положение и направление камеры в виде точки и стрелки.
    
    ax: объект 3D axes
    camera_pos: (3,) массив - позиция камеры в мировых координатах
    camera_forward: (3,) массив - направление взгляда камеры
    color: цвет рисования
    """
    # scatter() рисует точку в 3D пространстве
    ax.scatter(
        [camera_pos[0]], 
        [camera_pos[1]], 
        [camera_pos[2]],
        color=color, 
        s=200,               # размер точки
        marker='o',          # форма маркера (круг)
        edgecolors='black', 
        linewidths=2,
        label='Позиция камеры'
    )
    
    # quiver() рисует стрелку (вектор) от точки
    # параметры: начало_x, начало_y, начало_z, компонента_dx, компонента_dy, компонента_dz
    ax.quiver(
        camera_pos[0], camera_pos[1], camera_pos[2],
        camera_forward[0], camera_forward[1], camera_forward[2],
        color=color,
        arrow_length_ratio=0.2,  # длина стрелочки относительно вектора
        linewidth=3,
        label='Направление взгляда'
    )


def create_cube(pos, scale_factor=1.0):
    """
    Создает куб с заданной позицией и масштабом.
    
    pos: (3,) массив - позиция центра куба (x, y, z) в world space
    scale_factor: коэффициент масштабирования куба
    
    возвращает: (4, 8) матрица вершин куба в однородных координатах
    """
    # Базовый куб с вершинами от -1 до 1 по каждой оси
    vertices = np.array([
        [-1,  1,  1, -1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1, -1,  1,  1],
        [-1, -1, -1, -1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1,  1,  1,  1]
    ], dtype=float)
    
    # Применяем масштабирование: S * vertices
    S = scale_matrix(scale_factor, scale_factor, scale_factor)
    vertices = S @ vertices
    
    # Применяем трансляцию: T * S * vertices
    T = translate_matrix(pos[0], pos[1], pos[2])
    vertices = T @ vertices
    
    return vertices


def setup_axes_limits_and_labels(ax, limit=6, title="", view_azim=-37.5, view_elev=30):
    """
    Настраивает пределы осей, размер box'а, вид и подписи для 3D графика.
    
    ax: объект 3D axes
    limit: значение для set_xlim, set_ylim, set_zlim (от -limit до +limit)
    title: заголовок графика
    view_azim: азимут угла обзора (горизонтальный угол)
    view_elev: угол возвышения (вертикальный угол)
    """
    # set_box_aspect() делает куб "кубическим" (равные пропорции по всем осям)
    ax.set_box_aspect([1, 1, 1])
    
    # Устанавливаем пределы по осям
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)
    
    # view_init() устанавливает точку обзора
    # azim: горизонтальный угол вращения вокруг оси Z (в градусах)
    # elev: вертикальный угол возвышения (в градусах)
    ax.view_init(azim=view_azim, elev=view_elev)
    
    # set_*ticks() устанавливает сетку на осях
    ticks = np.linspace(-limit, limit, 5)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_zticks(ticks)
    
    # Подписи осей
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Заголовок подграфика
    ax.set_title(title, fontsize=11, fontweight='bold')


def main():
    """Основная программа для задания 6"""
    
    # ========== СОЗДАНИЕ СЦЕНЫ ==========
    # Создаем 3 кубика разных размеров в разных позициях
    cube1_vertices = create_cube([0, 0, 0], scale_factor=1.0)
    cube2_vertices = create_cube([2.5, 0, 0], scale_factor=0.8)
    cube3_vertices = create_cube([-2.5, 0, 0], scale_factor=0.6)
    
    # Матрица граней куба (индексы вершин, образующих каждую грань)
    faces_cube = np.array([
        [0, 1, 5, 4],  # передняя грань
        [1, 2, 6, 5],  # верхняя грань
        [2, 3, 7, 6],  # задняя грань
        [3, 0, 4, 7],  # нижняя грань
        [0, 1, 2, 3],  # левая грань
        [4, 5, 6, 7]   # правая грань
    ])
    
    # ========== ОПРЕДЕЛЕНИЕ КАМЕРЫ ==========
    print("\n" + "="*70)
    print("ЗАДАНИЕ 6: РЕАЛИЗАЦИЯ КАМЕРЫ И ПРЕОБРАЗОВАНИЕ В CAMERA SPACE")
    print("="*70)
    
    # Параметры камеры
    camera_pos = np.array([3.0, 4.0, 3.0])      # позиция камеры в world space
    camera_axis = np.array([1.0, 1.0, 1.0])     # ось поворота камеры (диагональ)
    camera_axis = camera_axis / np.linalg.norm(camera_axis)  # нормализуем
    camera_angle = -np.pi / 6                    # угол поворота (-30°)
    
    print(f"\nПараметры камеры:")
    print(f"  Позиция (world space): {camera_pos}")
    print(f"  Ось поворота: {camera_axis}")
    print(f"  Угол поворота: {np.degrees(camera_angle):.1f}°")
    
    # Вычисляем view-матрицу C^-1 (из world space в camera space)
    C_inv = view_matrix(camera_pos, camera_axis, camera_angle)
    
    # Обратная матрица C (для визуализации: из camera space в world space)
    C = np.linalg.inv(C_inv)
    
    print(f"\nМатрица вида (view matrix) C^-1:")
    pprint(np.round(C_inv, 4))
    
    print(f"\nМатрица камеры C:")
    pprint(np.round(C, 4))
    
    # Проверка: C @ C^-1 должна быть единичной матрицей
    identity_check = C @ C_inv
    print(f"\nПроверка: C @ C^-1 =")
    pprint(np.round(identity_check, 10))
    
    # ========== ВЫЧИСЛЕНИЕ НАПРАВЛЕНИЯ ВЗГЛЯДА КАМЕРЫ ==========
    
    # Получаем направление взгляда камеры в world space
    # В camera space камера смотрит в направлении -Z, преобразуем в world space
    camera_forward_world = (C @ np.array([0, 0, -1, 0]))[:3]
    
    # Вычисляем азимут: угол в XY плоскости от оси X
    # arctan2(y, x) дает угол
    azim_angle = np.arctan2(camera_forward_world[1], camera_forward_world[0])
    
    # Вычисляем возвышение: угол от XY плоскости до вектора
    # сначала находим длину проекции на XY плоскость
    xy_projection_length = np.sqrt(camera_forward_world[0]**2 + camera_forward_world[1]**2)
    # затем arctan2(z, xy_length)
    elev_angle = np.arctan2(camera_forward_world[2], xy_projection_length)
    
    print(f"\nНаправление взгляда камеры (world space): {camera_forward_world}")
    print(f"  Азимут: {np.degrees(azim_angle):.1f}°")
    print(f"  Возвышение: {np.degrees(elev_angle):.1f}°")
    
    # ========== ПРЕОБРАЗОВАНИЕ КУБИКОВ В CAMERA SPACE ==========
    
    # Преобразуем все кубики в camera space, применяя C^-1
    cube1_camera_space = C_inv @ cube1_vertices
    cube2_camera_space = C_inv @ cube2_vertices
    cube3_camera_space = C_inv @ cube3_vertices
    
    # ========== ВИЗУАЛИЗАЦИЯ ==========
    fig = plt.figure(figsize=(18, 5))
    
    # ===== ГРАФИК 1: Стандартный вид (world space) =====
    ax1 = fig.add_subplot(1, 4, 1, projection='3d', proj_type='ortho')
    
    # draw_shape() рисует каждый кубик на осях
    draw_shape(ax1, cube1_vertices, faces_cube, 'blue', alpha=0.7)
    draw_shape(ax1, cube2_vertices, faces_cube, 'cyan', alpha=0.7)
    draw_shape(ax1, cube3_vertices, faces_cube, 'magenta', alpha=0.7)
    
    # Рисуем позицию и направление камеры в world space
    draw_camera_frustum(ax1, camera_pos, camera_forward_world * 2, color='red')
    
    setup_axes_limits_and_labels(
        ax1, 
        limit=6, 
        title="1. Стандартный вид\n(World Space)",
        view_azim=-37.5, 
        view_elev=30
    )
    ax1.legend(fontsize=8, loc='upper right')
    
    # ===== ГРАФИК 2: Вид ИЗ позиции камеры, смотрим В НАПРАВЛЕНИИ её взгляда =====
    ax2 = fig.add_subplot(1, 4, 2, projection='3d', proj_type='ortho')
    
    draw_shape(ax2, cube1_vertices, faces_cube, 'blue', alpha=0.7)
    draw_shape(ax2, cube2_vertices, faces_cube, 'cyan', alpha=0.7)
    draw_shape(ax2, cube3_vertices, faces_cube, 'magenta', alpha=0.7)
    
    draw_camera_frustum(ax2, camera_pos, camera_forward_world * 2, color='red')
    
    setup_axes_limits_and_labels(
        ax2, 
        limit=6, 
        title="2. Вид из позиции камеры\n(смотрим В направлении взгляда)",
        view_azim=np.degrees(azim_angle), 
        view_elev=np.degrees(elev_angle)
    )
    ax2.legend(fontsize=8, loc='upper right')
    
    # ===== ГРАФИК 3: После применения C^-1 (camera space) =====
    ax3 = fig.add_subplot(1, 4, 3, projection='3d', proj_type='ortho')
    
    # Рисуем преобразованные кубики в camera space
    draw_shape(ax3, cube1_camera_space, faces_cube, 'blue', alpha=0.7)
    draw_shape(ax3, cube2_camera_space, faces_cube, 'cyan', alpha=0.7)
    draw_shape(ax3, cube3_camera_space, faces_cube, 'magenta', alpha=0.7)
    
    # В camera space камера находится в начале координат (0, 0, 0)
    # и смотрит в направлении -Z (вперед)
    ax3.scatter([0], [0], [0], color='red', s=200, marker='o', 
                edgecolors='black', linewidths=2, label='Камера')
    
    # quiver() рисует стрелку (вектор) от точки
    ax3.quiver(0, 0, 0, 0, 0, -1, color='red', arrow_length_ratio=0.3, 
               linewidth=3, label='Направление')
    
    setup_axes_limits_and_labels(
        ax3, 
        limit=6, 
        title="3. После C^-1\n(Camera Space)",
        view_azim=-37.5, 
        view_elev=30
    )
    ax3.legend(fontsize=8, loc='upper right')
    
    # ===== ГРАФИК 4: Вид почти сверху на Camera Space =====
    # Чтобы оси X и Y совпадали с графиком 2, используем одинаковые
    # азимут и возвышение. Вместо elev=-90 ставим очень высокое значение (80°)
    
    ax4 = fig.add_subplot(1, 4, 4, projection='3d', proj_type='ortho')
    
    draw_shape(ax4, cube1_camera_space, faces_cube, 'blue', alpha=0.7)
    draw_shape(ax4, cube2_camera_space, faces_cube, 'cyan', alpha=0.7)
    draw_shape(ax4, cube3_camera_space, faces_cube, 'magenta', alpha=0.7)
    
    ax4.scatter([0], [0], [0], color='red', s=200, marker='o', 
                edgecolors='black', linewidths=2, label='Камера')
    
    # Общий заголовок для всей фигуры
    fig.suptitle("Задание 6: Реализация камеры и преобразование в Camera Space", 
                 fontsize=13, fontweight='bold')
    
    # tight_layout() автоматически подгоняет отступы между подграфиками
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*70)
    print("ЗАВЕРШЕНО")
    print("="*70)


if __name__ == '__main__':
    main()
