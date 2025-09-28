from sympy import Matrix, zeros, pprint
from random import sample
from itertools import product


alphabet_dict = {
    'А': 0,
    'Б': 1,
    'В': 2,
    'Г': 3,
    'Д': 4,
    'Е': 5,
    'Ё': 6,
    'Ж': 7,
    'З': 8,
    'И': 9,
    'Й': 10,
    'К': 11,
    'Л': 12,
    'М': 13,
    'Н': 14,
    'О': 15,
    'П': 16,
    'Р': 17,
    'С': 18,
    'Т': 19,
    'У': 20,
    'Ф': 21,
    'Х': 22,
    'Ц': 23,
    'Ч': 24,
    'Ш': 25,
    'Щ': 26,
    'Ы': 27,
    'Э': 28,
    'Ю': 29,
    'Я': 30
}

reversed_alph_dict = dict(map(lambda x: x[::-1], alphabet_dict.items()))


def generate_vect_from_word(word: str) -> Matrix:
    return Matrix([alphabet_dict[s] for s in word])


def make_subvectors(v: Matrix, length: int) -> list:  # Поделить вектор на меньшие вектора
    subvectors = []
    start = 0
    for i in range(len(v) // length):
        subvectors.append(v[start:start + length, 0])
        start += length

    return subvectors


def mod(matrix: Matrix, mod: int = len(alphabet_dict)) -> Matrix: # функция взятия по модулю
    abs_matrix = matrix.copy()
    vects_row_idxs, vects_col_idxs = range(matrix.shape[0]), range(matrix.shape[1])
    for i, j in product(vects_row_idxs, vects_col_idxs):
        abs_matrix[i, j] %= mod
    return abs_matrix 


def Hill_cipher(key: Matrix, vect: Matrix) -> Matrix: # Шифр Хилла: умножаем и берем по модулю
    close_v = key @ vect
    close_v_abs = mod(close_v)
    return close_v_abs


def translate_from_vectors(vects_list: list) -> str: # генерация слова из векторов - сообщений
    message = ''
    vects_nums = range(len(vects_list))
    vects_row_idxs, vects_col_idxs = range(vects_list[0].shape[0]), range(vects_list[0].shape[1])
    for p, i, j in product(vects_nums, vects_row_idxs, vects_col_idxs):
        message += reversed_alph_dict[vects_list[p][i, j]]
    return message


def generate_key(size: int) -> Matrix:
    random_elements = sample(sorted(alphabet_dict.keys()), k=size*size)
    row_idxs, col_idxs = range(size), range(size)
    key = zeros(size)
    for i, j in product(row_idxs, col_idxs):
        key[i, j] = alphabet_dict[random_elements.pop()]
    if key.det() % len(alphabet_dict) == 0:
        generate_key(size)
    else:
        return key


def start_coding(key: Matrix, p: Matrix, show_subvs: bool = False) -> str: # Функция выполнения кодирования с выводом информации в консоль
    print(f'\n============================================')
    subvectors = make_subvectors(p, key.shape[1])
    if show_subvs:
        print()
        pprint(subvectors)

    close_vectors = []
    for subv in subvectors:
        close_v = Hill_cipher(key, subv)
        close_vectors.append(close_v)
    
    cipher_word = translate_from_vectors(close_vectors)
    print('Зашифрованное сообщение: ', ' '.join(cipher_word))
    print(f'============================================\n')
    return cipher_word


def start_decoding(key: Matrix, c: Matrix, show_subvs: bool = False) -> str:  # Функция декодирования и pretty вывода информации в консоль
    print('\n============================================')
    reversed_key = key.inv_mod(len(alphabet_dict))
    subvectors = make_subvectors(c, key.shape[1])

    if show_subvs:
        print()
        pprint(subvectors)

    open_vectors = []
    for subv in subvectors:
        open_v = Hill_cipher(reversed_key, subv)
        open_vectors.append(open_v)
    
    decode_cipher_word = translate_from_vectors(open_vectors)
    print('Расшифрованное сообщение:', ' '.join(decode_cipher_word))
    print('============================================\n')
    return decode_cipher_word


def repair_key(open_word: str, close_word: str, key_size: int, show_annot: bool = False) -> Matrix:
    open_subvs = make_subvectors(generate_vect_from_word(open_word), key_size)
    close_subvs = make_subvectors(generate_vect_from_word(close_word), key_size)
    if show_annot:
        print("============================================")
        print("Процесс восстановления ключа:")
        print("Исходные вектора\n")
        pprint(open_subvs)
        print("\nЗашифрованные вектора\n")
        pprint(close_subvs)

    random_idx_i, random_idx_j = sample(range(len(open_subvs)), 2)
    p = open_subvs[random_idx_i].row_join(open_subvs[random_idx_j])
    c = close_subvs[random_idx_i].row_join(close_subvs[random_idx_j])
    while p.det() % len(alphabet_dict) == 0 or c.det() % len(alphabet_dict) == 0:
        random_idx_i, random_idx_j = sample(range(len(open_subvs)), 2)
        p = open_subvs[random_idx_i].row_join(open_subvs[random_idx_j])
        c = close_subvs[random_idx_i].row_join(close_subvs[random_idx_j])

    if show_annot:
        print("\nВыбранные вектора для матриц P и С (K = C * P**-1):\n")
        pprint([p, c])

    reverse_p = p.inv_mod(len(alphabet_dict))
    repaired_key = mod(c @ reverse_p)

    if show_annot:
        print("\nПолученный ключ:\n")
        pprint(repaired_key)
        print("============================================\n")    
               
    return repaired_key


word1 = 'АББРЕВИАТУРА'
with open('lab-1/word.txt', 'r', encoding='utf-8') as f:
    word2 = ''
    for el in f.readline():
        word2 += el.upper()


key = generate_key(2)  # Бог его знает какой, обратимый, ключ.

cipher_word1 = start_coding(key, generate_vect_from_word(word1))  # Известное зашифрованное слово
decode_word1 = start_decoding(key, generate_vect_from_word(cipher_word1))  # Известное исходное слово


#-------------------------
# Для восстановления ключа возьмём два случайных ЛНЗ вектора сообщения от зашифрованного и исходного слова (индексы должены совпадать!)
# Составим из них матрицы 2x2 P(исходные векторы) и С(зашифрованные векторы) в столбцах которых будут взятые векторы.
# Останется найти ключ по следующей формуле: K = C * P^-1
#-------------------------
repaired_key = repair_key(decode_word1, cipher_word1, key.shape[1])  # Восстановление ключа

cipher_word2 = start_coding(key, generate_vect_from_word(word2))
decode_word2 = start_decoding(repaired_key, generate_vect_from_word(cipher_word2))


