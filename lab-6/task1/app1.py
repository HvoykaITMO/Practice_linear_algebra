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


def load_picture(path, rs):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    m, n = img.shape
    total_memory = m * n
    print(f"Количество чисел для хранения исходной матрицы: {total_memory}")

    S = np.linalg.svd(img, compute_uv=False)
    print(f"Максимальное количество ненулевых сингулярных чисел: {S.shape[0]}")

    memory_amount = []
    percent_memory = []

    for r in rs:
        U, S, Vh = np.linalg.svd(img, full_matrices=False)
        U, S, Vh = cut_singular_values(U, S, Vh, k=r)
        img_new = rebuild_matrix_from_SVD(U, S, Vh).astype(np.uint8)

        memory = m*r + r + r*n
        memory_amount.append(memory)
        percent_memory.append(round(memory / total_memory * 100, 2))

        cv2.imshow(f"r = {r}", img_new)
        cv2.imwrite(f"results/r{r}.jpg", img_new)
    df = pd.DataFrame({"Количество Синг.ч.": rs,"Чисел для хранения в памяти": memory_amount, "Степень сжатия": percent_memory})
    print(df)
    cv2.waitKey(0)