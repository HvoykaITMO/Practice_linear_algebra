import numpy as np
from scipy.linalg import expm


def scale_matrix(sx, sy, sz):
    """Матрица масштабирования"""
    return np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1],
    ], dtype=float)


def translate_matrix(tx, ty, tz):
    """Матрица сдвига"""
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],
    ], dtype=float)


def rotation_matrix(v, theta):
    """
    R_v(theta) = exp(J * theta)
    v: вектор оси (3,) NumPy array
    theta: угол в радианах (float)
    возвращает: (4, 4) NumPy array
    """
    vx, vy, vz = v
    norm_v = np.linalg.norm(v)
    
    if norm_v == 0:
        raise ValueError("Вектор оси не может быть нулевым")
    
    # Генератор вращения J (4x4)
    J = (1 / norm_v) * np.array([
        [0,   -vz,  vy,  0],
        [vz,   0,  -vx,  0],
        [-vy,  vx,   0,  0],
        [0,    0,    0,  0]
    ], dtype=float)
    
    # R_v(theta) = exp(J * theta)
    R = expm(J * theta)
    
    return R


def rotation_around_point(v, theta, M):
    """
    Поворот вокруг оси, проходящей через точку M с направлением v.
    
    Формула: R_M = T(M) * R_v(theta) * T(-M)
    
    v: направление оси (3,) array
    theta: угол в радианах
    M: точка в 3D (3,) array или однородные координаты (4,)
    
    возвращает: (4, 4) матрица поворота
    """
    # Если M в однородных координатах, извлекаем (x, y, z)
    if len(M) == 4:
        M3 = M[:3] / M[3]
    else:
        M3 = M
    
    # Матрицы трансляции
    T_plus = translate_matrix(M3[0], M3[1], M3[2])
    T_minus = translate_matrix(-M3[0], -M3[1], -M3[2])
    
    # Матрица поворота вокруг начала координат
    R_center = rotation_matrix(v, theta)
    
    # Композиция: R_M = T(M) * R_v(theta) * T(-M)
    R_M = T_plus @ R_center @ T_minus
    
    return R_M


def view_matrix(camera_position, camera_rotation_axis, camera_rotation_angle):
    """
    Вычисляет view-матрицу C^{-1}, которая преобразует из world space в camera space.
    
    Формула: C^{-1} = R^T * T(-camera_position)
    
    camera_position: (3,) array — позиция камеры в мировых координатах
    camera_rotation_axis: (3,) array — ось поворота камеры
    camera_rotation_angle: float — угол поворота камеры в радианах
    
    возвращает: (4, 4) view matrix
    """
    # Матрица поворота камеры
    R_camera = rotation_matrix(camera_rotation_axis, camera_rotation_angle)
    
    # Транспонируем блок вращения 3x3 (инверсия поворота)
    R_inv = R_camera.copy()
    R_inv[:3, :3] = R_camera[:3, :3].T
    
    # Сдвиг на -camera_position
    T_neg = translate_matrix(-camera_position[0], -camera_position[1], -camera_position[2])
    
    # View matrix = R^T * T(-pos)
    C_inv = R_inv @ T_neg
    
    return C_inv
