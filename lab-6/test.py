import numpy as np
import cv2 as cv


def cut_singular_values(U, S, Vh, k):
    if k == len(S):
        print("Attention: k = amount of singular values")
    indx = -1 * k
    return U[:, :indx], S[:indx], Vh[:indx, :]


def rebuild_matrix_from_SVD(U, S, Vh):
    return U @ np.diag(S) @ Vh


A = np.array([[1000,0,0,0],[0,17968,24024,0],[0,-24024,-31982, 0]])
m, n = A.shape

U, S, Vh = np.linalg.svd(A, full_matrices=False)


print(A)
print()
U, S, Vh = cut_singular_values(U, S, Vh, 3)
print(rebuild_matrix_from_SVD(U, S, Vh))