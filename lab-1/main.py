from sympy import Matrix, pprint
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


def gcd(a, b):  # Алгоритм Евклида
    while b != 0:
        a, b = b, a % b
    return a


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
    vects_row_idxs, vect_col_idxs = range(matrix.shape[0]), range(matrix.shape[1])
    for i, j in product(vects_row_idxs, vect_col_idxs):
        abs_matrix[i, j] %= mod
    return abs_matrix    


def Hill_cipher(key: Matrix, vect: Matrix) -> Matrix: # Шифр Хилла: умножаем и берем по модулю
    close_v = key @ vect
    close_v_abs = mod(close_v)
    return close_v_abs


def translate_from_vectors(vects_list: list) -> str:
    message = ''
    vects_nums = range(len(vects_list))
    vects_row_idxs, vects_col_idxs = range(vects_list[0].shape[0]), range(vects_list[0].shape[1])
    for p, i, j in product(vects_nums, vects_row_idxs, vects_col_idxs):
        message += reversed_alph_dict[vects_list[p][i, j]]
    return message

def start_coding(num: int, key: Matrix, p: Matrix) -> None:
    print(f'\n{num})------------------------------------------\n')
    subvectors = make_subvectors(P, key.shape[1])
    
    print('\nВекторы - сообщение:\n')
    pprint(subvectors)
    
    print('\nКлюч:\n')
    pprint(key)

    close_vectors = []
    for subv in subvectors:
        close_v = Hill_cipher(key, subv)
        close_vectors.append(close_v)
        
    print('\nЗашифрованные вектора - сообщение:\n')
    pprint(close_vectors)
    
    cipher_word = translate_from_vectors(close_vectors)
    print('\nЗашифрованное сообщение:', cipher_word)
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    return cipher_word
    
    
def damage_cipher_word(word)
    


#------------------
# Шифр Хилла
#------------------
word = 'ПРОСТРАНСТВО'
print('Исходное сообщение:', word)
    
P = generate_vect_from_word(word) # Сообщение из 12 символов

#------------------------------
K1 = Matrix([[alphabet_dict['К'], alphabet_dict['Ы']], 
             [alphabet_dict['У'], alphabet_dict['Ц']]])
assert K1.det() != 0
#------------------------------
#------------------------------
K2 = Matrix([[alphabet_dict['М'], alphabet_dict['Л'], alphabet_dict['К']],
            [alphabet_dict['Т'], alphabet_dict['Я'], alphabet_dict['Х']],
            [alphabet_dict['Ч'], alphabet_dict['Щ'], alphabet_dict['З']]])
assert K2.det() != 0
#------------------------------
#------------------------------
K3 = Matrix([[alphabet_dict['Ч'], alphabet_dict['Г'], alphabet_dict['П'], alphabet_dict['Ф']],
            [alphabet_dict['Д'], alphabet_dict['Ж'], alphabet_dict['Й'], alphabet_dict['Ш']],
            [alphabet_dict['И'], alphabet_dict['А'], alphabet_dict['Э'], alphabet_dict['К']],
            [alphabet_dict['Ю'], alphabet_dict['О'], alphabet_dict['Ы'], alphabet_dict['Н']]])
assert K3.det() != 0
#------------------------------


cipher_word_k1 = start_coding(num=1, key=K1, p=P)
cipher_word_k2 = start_coding(num=2, key=K2, p=P)
cipher_word_k3 = start_coding(num=3, key=K3, p=P)
