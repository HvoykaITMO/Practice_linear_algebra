import numpy as np
import pandas as pd
import pymorphy3
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from collections import Counter


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


def rebuild_matrix_from_SVD(U, S, Vh):
    return np.clip(U @ np.diag(S) @ Vh, 0, 255).astype(np.uint8)  # с Защитой от переполнения


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
    print("Первые два сингулярных числа:", S[:2], end='\n\n')  # Первые два сингулярных числа
    Us = pd.DataFrame(U[:, :2] , columns=["Theme_1", "Theme_2"], index=term_doc_matrix_df.index)
    print(Us, end='\n\n')
    Vhs = pd.DataFrame(Vh[:2, :], columns=cols, index=["Theme_1", "Theme_2"]).T
    print(Vhs)
    ###########################################################




