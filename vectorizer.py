import numpy as np
from typing import Literal
from scipy.sparse import spmatrix

# Algorithme pour la vectorisation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

from json_treatment import json_load

"""
def vectorize(input_path : str,algorithm_name : Literal["tf-idf","bow"] = "tf-idf")-> None :
    texts = data_load(input_path,"text")
    if algorithm_name == "tf-idf" :
        vectors = tfidf(texts)
        pass
    pass
"""

def tfidf(texts : list[str], norm : bool = False) -> np.ndarray:
    tfidf = TfidfVectorizer(ngram_range=(1, 2), stop_words=json_load("stopwords.json"))
    vectors = tfidf.fit_transform(texts)
    grams = tfidf.get_feature_names_out()
    if len(grams) > 500 :
        svd = TruncatedSVD(n_components=50, random_state=42)
        vectors = svd.fit_transform(vectors)
    if norm :
        normalizer = Normalizer(copy=False)
        vectors = normalizer.fit_transform(vectors)
    if isinstance(vectors,spmatrix) :
        return vectors.toarray()
    else :
        return vectors

def bag_of_words(texts : list[str], norm : bool = False) -> np.ndarray:
    bow = CountVectorizer(ngram_range=(1, 2), stop_words=json_load("stopwords.json"))
    vectors = bow.fit_transform(texts)
    grams = bow.get_feature_names_out()
    if len(grams) > 500 :
        svd = TruncatedSVD(n_components=50, random_state=42)
        vectors = svd.fit_transform(vectors)
    if norm :
        normalizer = Normalizer(copy=False)
        vectors = normalizer.fit_transform(vectors)
    if isinstance(vectors,spmatrix) :
        return vectors.toarray()
    else :
        return vectors