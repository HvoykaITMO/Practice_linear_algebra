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
