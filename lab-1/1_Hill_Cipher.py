from sympy import Matrix, pprint, latex
from itertools import product
from random import sample


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

    print('\nВекторы - сообщение:\n')
    pprint(subvectors)

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


def start_coding(key: Matrix, p: Matrix, num: int = 0) -> str: # Функция выполнения кодирования с выводом информации в консоль
    print(f'\n{num})------------------------------------------')
    subvectors = make_subvectors(p, key.shape[1])
    
    print('\nКлюч:\n')
    pprint(key)

    close_vectors = []
    for subv in subvectors:
        close_v = Hill_cipher(key, subv)
        close_vectors.append(close_v)
        
    print('\nЗашифрованные вектора - сообщение:\n')
    pprint(close_vectors)
    
    cipher_word = translate_from_vectors(close_vectors)
    print('\nЗашифрованное сообщение:', ' '.join(cipher_word))
    print(f'-------------------------------------------\n')
    return cipher_word
    
    
def damage_cipher_word(word: str, k: int) -> str:  # Функция повреждения сообщения с выводом полезных фактов в консоль
    print('\n############################################')
    print('Зашифрованное сообщение:', ' '.join(word))
    damage_word = list(word)
    dict_letter_idxs = sample(sorted(alphabet_dict.values()), k)
    word_replace_idxs = sample(list(range(len(word))), k)
    for u, v in zip(word_replace_idxs, dict_letter_idxs):
        print(f'Замена: {damage_word[u]} -> {reversed_alph_dict[v]}')
        damage_word[u] = reversed_alph_dict[v]
        
    damage_word = ''.join(damage_word)
    print('Искажённое сообщение:' + ' '*(len('Зашифрованное сообщение:') - len('Искажённое сообщение:')), ' '.join(damage_word))
    print('############################################\n')
    return damage_word


def start_decoding(key: Matrix, c: Matrix) -> str:  # Функция декодирования и pretty вывода информации в консоль
    print('\n============================================')
    print('Дешифрую слово:', ' '.join(translate_from_vectors([c])))
    reversed_key = key.inv_mod(len(alphabet_dict))
    subvectors = make_subvectors(c, key.shape[1])

    print('\nОбратный ключ:\n')
    pprint(reversed_key)

    open_vectors = []
    for subv in subvectors:
        open_v = Hill_cipher(reversed_key, subv)
        open_vectors.append(open_v)
        
    print('\nРасшифрованные вектора - сообщение:\n')
    pprint(open_vectors)
    
    decode_cipher_word = translate_from_vectors(open_vectors)
    print('\nРасшифрованное сообщение:', ' '.join(decode_cipher_word))
    print('============================================\n')
    return decode_cipher_word

        
word = 'ПРОСТРАНСТВО'
print('Исходное сообщение:', ' '.join(word))

# Задаём наши ключи. Если их определитель равен нулю, получим ошибку
K1 = Matrix([[alphabet_dict['К'], alphabet_dict['Ы']], 
             [alphabet_dict['У'], alphabet_dict['Ц']]])
assert K1.det() % len(alphabet_dict) != 0
K2 = Matrix([[alphabet_dict['М'], alphabet_dict['Л'], alphabet_dict['К']],
            [alphabet_dict['Т'], alphabet_dict['Я'], alphabet_dict['Х']],
            [alphabet_dict['Ч'], alphabet_dict['Щ'], alphabet_dict['З']]])
assert K2.det() % len(alphabet_dict) != 0
K3 = Matrix([[alphabet_dict['Ч'], alphabet_dict['Г'], alphabet_dict['П'], alphabet_dict['Ф']],
            [alphabet_dict['Д'], alphabet_dict['Ж'], alphabet_dict['Й'], alphabet_dict['Ш']],
            [alphabet_dict['И'], alphabet_dict['А'], alphabet_dict['Э'], alphabet_dict['К']],
            [alphabet_dict['Ю'], alphabet_dict['О'], alphabet_dict['Ы'], alphabet_dict['Н']]])
assert K3.det() % len(alphabet_dict) != 0

# Шифруем наше сообщение различными ключами
cipher_word_K1 = start_coding(key=K1, p=generate_vect_from_word(word), num=1)
cipher_word_K2 = start_coding(key=K2, p=generate_vect_from_word(word), num=2)
cipher_word_K3 = start_coding(key=K3, p=generate_vect_from_word(word), num=3)

# Искажаем зашифрованные сообщения
damage_word_K1 = damage_cipher_word(word=cipher_word_K1, k=3)
damage_word_K2 = damage_cipher_word(word=cipher_word_K2, k=3)
damage_word_K3 = "ЯЗСГЩСОЙУКЁР"

# Дешифруем искажённые сообщения
start_decoding(key=K1, c=generate_vect_from_word(damage_word_K1))
start_decoding(key=K2, c=generate_vect_from_word(damage_word_K2))
start_decoding(key=K3, c=generate_vect_from_word(damage_word_K3))