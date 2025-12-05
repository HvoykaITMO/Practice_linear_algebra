import numpy as np
from copy import deepcopy
from sympy import Matrix


def to_h(point3):
    x, y, z = point3
    return Matrix([x, y, z, 1])

def from_h(point4):
    x, y, z, w = point4
    return Matrix([x/w, y/w, z/w])

def transform_points(points3, M):
    new_points = deepcopy(points3)
    for i in range(points3.shape[1]):
        new_points[:, i] = M @ points3[:, i]
    return new_points