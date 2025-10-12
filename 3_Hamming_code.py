from sympy import pprint, Matrix
from random import choices


HAMMING_ALL_BITS, HAMMING_INFO_BIT = 7, 4

BINARY_MATCH = {
    'А': '00000',
    'Б': '00001',
    'В': '00010',
    'Г': '00011',
    'Д': '00100',
    'Е': '00101',
    'Ж': '00110',
    'З': '00111',
    'И': '01000',
    'Й': '01001',
    'К': '01010',
    'Л': '01011',
    'М': '01100',
    'Н': '01101',
    'О': '01110',
    'П': '01111',
    'Р': '10000',
    'С': '10001',
    'Т': '10010',
    'У': '10011',
    'Ф': '10100',
    'Х': '10101',
    'Ц': '10110',
    'Ч': '10111',
    'Ш': '11000',
    'Щ': '11001',
    'Ъ': '11010',
    'Ы': '11011',
    'Ь': '11100',
    'Э': '11101',
    'Ю': '11110',
    'Я': '11111'
}

REVERSED_BINARY_MATCH = dict(map(lambda x: x[::-1], BINARY_MATCH.items()))


# Переводим слово в биты
def binarization(word: str, show_annot: bool = False) -> str:
    if show_annot:
        print("-----------------------------------------------")
        print(f"Переводим слово {word} в битовое представление:\n")
    binary_word = [BINARY_MATCH[letter] for letter in word]
    binary_word = ''.join(binary_word)
    if show_annot:
        print(binary_word)
        print("-----------------------------------------------")
    return binary_word


# Разделение на "пачки" битов, не будем усложнять, поэтому предположим, что длина кода всегда делится на length.
# Одновременно с этим переводим пачки в векторы.
def translate_to_binary_vectors(code: str, length: int) -> tuple:
    binary_stack = []
    start = 0
    while start < len(code):
        struct_v = list(map(lambda x: [int(x)], code[start:start+length]))
        binary_stack.append(Matrix(struct_v))
        start += length
    print("-----------------------------------------------")
    print("Разобьём двоичное представление слова на векторы высоты 4.")
    print("Упорядоченный набор будет выглядеть следующим образом:\n")
    pprint(tuple(binary_stack))
    return tuple(binary_stack)


# Переводим векторы в одну слово
def translate_to_word(R: Matrix, binary_vectors: tuple, show_annot: bool = False) -> str:
    if show_annot:
        print("-----------------------------------------------")
        print("Превратим векторы в слово:\n")
    binary_word = ""
    for el in binary_vectors:
        l = R * el
        code = ''.join(list(map(lambda x: str(x), l)))
        binary_word += code

    new_word = ''
    start = 0
    step = 5  # длина кодовых слов в словаре
    while start < len(binary_word):
        code = binary_word[start:start+step]
        new_word += REVERSED_BINARY_MATCH[code]
        start += step
    if show_annot:
        print(f"{binary_word} -> {new_word}")
        print("-----------------------------------------------")
    return new_word


# Взятие результата по модулю 2
def binary_mod(A: Matrix) -> Matrix:
    return A.applyfunc(lambda x: x % 2)


# Процесс кодирования вектора
def Hamming(C: Matrix, v: Matrix) -> Matrix:
    u = binary_mod(C * v)
    return u


# Искажает amount случайных, битов
def damage_bits(binary_vectors: tuple, amount: int, show_annot: bool = False) -> tuple:
    if show_annot:
        print("-----------------------------------------------")
        print("Исказим биты набора векторов.")
        print("Сделаем это так, чтобы не исказилось два бита в одном векторе.")
        print("Исходный набор:\n")
        pprint(binary_vectors)
    damaged_vectors = list(binary_vectors)
    idxs = choices(range(HAMMING_ALL_BITS), k=amount)
    for i, v in enumerate(damaged_vectors):
        if len(idxs) != 0:
            idx = idxs.pop()
        else:
            continue
        if show_annot:
            print(f"У {i + 1} вектора набора инвертирую бит на позиции {idx + 1}")
        v[idx] = (v[idx] + 1) % 2
    damaged_vectors = tuple(damaged_vectors)
    if show_annot:
        print("\nРезультат:")
        print("Было:\n")
        pprint(binary_vectors)
        print("Стало:\n")
        pprint(damaged_vectors)
        print("-----------------------------------------------")
    return damaged_vectors


# Реализация кодирования целого слова
def start_codding(C: Matrix, binary_vectors: tuple) -> tuple:
    print("-----------------------------------------------")
    print("Используем матрицу C для кодирования векторов.")
    coded_vectors = []
    for v in binary_vectors:
        u = Hamming(C.T, v)
        coded_vectors.append(u)
    print("В результате получим следующий набор:\n")
    pprint(tuple(coded_vectors))
    print("-----------------------------------------------")
    return tuple(coded_vectors)

# Использование матрицы H и поиск ошибок
def get_sindroms(H: Matrix, binary_vectors: tuple, show_annot: bool = False) -> tuple:
    if show_annot:
        print("-----------------------------------------------")
        print("Используем матрицу H для получения синдромов.")
    decoded_vectors = []
    for u in binary_vectors:
        v = Hamming(H, u)
        decoded_vectors.append(v)
    if show_annot:
        print("В результате получим следующий набор синдромов:\n")
        pprint(tuple(decoded_vectors))
        print("-----------------------------------------------")
    return tuple(decoded_vectors)


def find_mistake_in_vectors(H: Matrix, binary_vectors: list) -> tuple:
    print("-----------------------------------------------")
    print("Проверим векторы на наличие ошибок в битах, умножив каждый на матрицу H и получив синдромы:\n")
    decoded_vectors = get_sindroms(H, binary_vectors)
    print("Результат:\n")
    pprint(decoded_vectors)
    print()
    error_idxs = []
    for i, v in enumerate(decoded_vectors):
        if not v.is_zero_matrix:
            binary_num = int(''.join(list((map(lambda x: str(x), v)))[::-1]), base=2)  # значения битов в матрице H идут в обратном порядке
            error_idxs.append((i, binary_num - 1))
            print(f"Найдена ошибка в {i+1}-ом векторе набора. Неверный - {binary_num} бит.")
    print("-----------------------------------------------")
    return tuple(error_idxs)


def correction_vectors(binary_vectors: tuple, error_idxs: tuple) -> tuple:
    print("-----------------------------------------------")
    print("Исправим векторы:\n")
    print("Исходный набор:\n")
    pprint(binary_vectors)
    print()
    binary_vectors = (binary_vectors[:])
    for i, j in error_idxs:
        print(f"В {i+1}-ом векторе меняем {j+1} бит")
        binary_vectors[i][j] = (binary_vectors[i][j] + 1) % 2
    print("\nИсправленный набор:\n")
    pprint(binary_vectors)
    print("\nПроверим, что всё верно исправлено, снова умножив на матрицу H:\n")
    pprint(get_sindroms(H, damaged_vectors))
    print("-----------------------------------------------\n")
    return binary_vectors


#  Зададим интересное слово из 4 букв:
word = "КРЫМ"
print("Выберем слово", word)

# C - матрица образов инф. битов и контрольн. битов
C = Matrix([
    [1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 1]
])

# H - матрица проверки на чётность
H = Matrix([
    [1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1]
    ])

# R - матрица декодирования
R = Matrix([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1]
])

binary_word = binarization(word, show_annot=True)
binary_vectors = translate_to_binary_vectors(binary_word, HAMMING_INFO_BIT)
coded_vectors = start_codding(C, binary_vectors)


DAMAGED_BIT_AMOUNT = 4  # Выбор количества искажаемых бит


damaged_vectors = damage_bits(coded_vectors, DAMAGED_BIT_AMOUNT, show_annot=True)
sindroms = get_sindroms(H, damaged_vectors, show_annot=True)
error_idxs = find_mistake_in_vectors(H, damaged_vectors)
recover_vectors = correction_vectors(damaged_vectors, error_idxs)

new_word = translate_to_word(R, recover_vectors, show_annot=True)
