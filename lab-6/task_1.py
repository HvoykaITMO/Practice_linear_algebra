import numpy as np
import pandas as pd
import cv2


def cut_singular_values(U, S, Vh, k):
    r = S.shape[0]
    if k < 0 or k >= r:
        return U, S, Vh

    Uk = U[:, :k]
    Sk = S[:k]
    Vhk = Vh[:k, :]
    return Uk, Sk, Vhk


def rebuild_matrix_from_SVD(U, S, Vh):
    return np.clip(U @ np.diag(S) @ Vh, 0, 255).astype(np.uint8)  # с Защитой от переполнения


cat = cv2.imread('cat.jpg', cv2.IMREAD_GRAYSCALE)
m, n = cat.shape
total_memory = m * n
print(f"Количество чисел для хранения исходной матрицы: {total_memory}")
rs = [360, 300, 240, 180, 120, 60, 20, 10, 1]
memory_amount = []
percent_memory = []
for r in rs:
    U, S, Vh = np.linalg.svd(cat, full_matrices=False)
    U, S, Vh = cut_singular_values(U, S, Vh, k=r)
    cat_new = rebuild_matrix_from_SVD(U, S, Vh).astype(np.uint8)

    memory = m*r + r + r*n
    memory_amount.append(memory)
    percent_memory.append(round(memory / total_memory * 100, 2))

    cv2.imshow(f"Cat (r = {r})", cat_new)
df = pd.DataFrame({"Количество Синг.ч.": rs,"Количество чисел для хранения в памяти": memory_amount, "Степень сжатия": percent_memory})
print(df)
cv2.waitKey(0)