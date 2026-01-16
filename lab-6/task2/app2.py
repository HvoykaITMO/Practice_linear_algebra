from fileinput import filename

import numpy as np
import pandas as pd
import pymorphy3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# pd.set_option('display.max_rows', None)       # показывать все строки
# pd.set_option('display.max_columns', None)    # показывать все столбцы
# pd.set_option('display.width', 120)           # ширина "экрана" в символах
# pd.set_option('display.max_colwidth', None)   # не обрезать текст в ячейках
# pd.set_option('display.precision', 3)         # число знаков после запятой

nltk.download("stopwords")
russian_stopwords = set(stopwords.words("russian"))
russian_stopwords.add("который")
tokenizer = RegexpTokenizer(r"\w+")
morph = pymorphy3.MorphAnalyzer()


def count_word_freq(document: list) -> Counter:  # Словарь слов
    return Counter(document)


def tokenize_no_punct(text: str) -> list:
    return tokenizer.tokenize(text.lower())  # Токенизация без пунктуации


def lemmatize_words(words: list) -> list:  # Приводим к начальной форме
    return [morph.parse(word)[0].normal_form for word in words]


def tokenize_no_stopwords(text: list) -> list:
    return [t for t in text if t not in russian_stopwords]  # Убираем предлоги, союзы и прочие стоп-слова.


def read_source(path: str) -> list:
    with open(path, encoding="utf8") as f:
        documents = eval(f.read())
    return documents


def cut_singular_values(U, S, Vh, k):
    r = S.shape[0]
    if k < 0 or k >= r:
        return U, S, Vh

    Uk = U[:, :k]
    Sk = S[:k]
    Vhk = Vh[:k, :]
    return Uk, Sk, Vhk


def make_cloud(weights, title, filename):
    wc = WordCloud(width=800, height=400,
                   background_color="white")
    wc = wc.fit_words(weights)
    plt.figure(figsize=(8, 4))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.savefig("results/" + filename + ".png")
    plt.show()


if __name__ == "__main__":
    docs = read_source("sources/data16.txt")

    for i in range(len(docs)):
        tokens = tokenize_no_punct(docs[i])  # Убрали пунктуацию
        tokens = lemmatize_words(tokens)  # Привели к начальной форме
        tokens = tokenize_no_stopwords(tokens)  # Убрали стоп-слова
        docs[i] = tokens

    all_words_freq = Counter()  # Сounter со всеми словами и их частотой (частота по всем документам)
    for doc in docs:
        all_words_freq.update(doc)

    all_doc_vectors = []
    for doc in docs:
        doc_words_freq = count_word_freq(doc)  # Частота слов в документе
        doc_vector = {k: doc_words_freq[k] for k in all_words_freq.keys()}
        all_doc_vectors.append(doc_vector)

    cols =[f"doc_{i}" for i in range(len(docs))]

    term_doc_matrix_df = pd.DataFrame(all_doc_vectors, index=cols).T  # Терм-документная матрица (DataFrame)

    term_doc_matrix_np = term_doc_matrix_df.to_numpy()

    U, S, Vh = np.linalg.svd(term_doc_matrix_np, full_matrices=False)


    ###########################################################
    # Первые два левых и правых вектора, а также соответствующе им сингулярные числа:
    U, S, Vh = cut_singular_values(U, S, Vh, 2)

    print("Первые два сингулярных числа:", S[:2], end='\n\n')  # Первые два сингулярных числа
    Us = pd.DataFrame(U , columns=["Theme_1", "Theme_2"], index=term_doc_matrix_df.index)
    Vhs = pd.DataFrame(Vh, columns=cols, index=["Theme_1", "Theme_2"]).T

    print(Us, end='\n\n')
    print(Vhs, end='\n\n')

    # Отсортированные по убыванию
    print(Us["Theme_1"].sort_values(ascending=False), end='\n\n')
    print(Us["Theme_2"].sort_values(ascending=False), end='\n\n')
    print(Vhs["Theme_1"].sort_values(ascending=False), end='\n\n')
    print(Vhs["Theme_2"].sort_values(ascending=False), end='\n\n')
    ###########################################################


    ###########################################################
    # Облако слов:
    weights_1 = Us["Theme_1"].sort_values(ascending=False).abs()
    weights_2 = Us["Theme_2"].sort_values(ascending=False).abs()

    make_cloud(weights_1, "Тема 1", filename="Wordcloud_theme_1")
    make_cloud(weights_2, "Тема 2", filename="Wordcloud_theme_2")
    ###########################################################