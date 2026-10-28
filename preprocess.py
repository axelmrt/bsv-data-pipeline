from pdf_extract import repertory_extract
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import pandas as pd
import numpy as np

####### Variable Globales #######
nlp = spacy.load("fr_core_news_lg") # Pipeline NLP complète (nlp.pipenames)


#Dataframe processing
def df_create(path : str) -> pd.DataFrame :
    """A partir d'un fichier on met toutes les données dans un dataframe par paragraphe"""
    pdf_text = repertory_extract(path)
    test = pd.DataFrame(pdf_text).T
    return test

def concat_columns(df : pd.DataFrame , column1 : str,column2 : str, separateur : str = " " ) -> pd.DataFrame :
    """On concatène 2 colonnes du dataframe dans une seule (dans la première)"""
    df[column1] = df[column1].astype(str) + separateur + df[column2].astype(str)
    df = df.drop(columns = column2)
    return df

def spacy_title_context_concat(df : pd.DataFrame) -> pd.DataFrame:
    """Concatène 2 colonnes du dataframe avec un titres similaires (comparaison avec cosine_similarity)"""
    titres = df.columns.to_numpy()
    vectors = [np.array([nlp(titre).vector]) for titre in titres]   #Array 2D nécessaire pour le cosine_similarity
    for i in range(len(vectors)) :
        v = vectors[i]
        for j in range(i + 1, len(vectors)):
            u = vectors[j]
            cos = cosine_similarity(v,u)
            if(cos > 0.9) and not np.array_equal(u, v) :
                df = concat_columns(df,titres[i],titres[j])
    return df

def spacy_data_context_concat(df : pd.DataFrame) -> pd.DataFrame :
    
    pass

#Text Processing
def spacy_word_tokenize(text : str, lemma : bool = False)-> list[str] :
    """Transforme le texte en liste de mot/ponctuation qui le compose\n
        lemma = True -> traitement lexical pour simplifier les mots"""
    doc = nlp(text)
    res = []
    for token in doc :
        if lemma :
            res.append(token.lemma_)
        else :
            res.append(token)
    return res

def spacy_sents_tokenize(text : str)-> list[str] :
    """Transforme le texte en liste de phrase qui le compose"""
    doc = nlp(text)
    res = []
    for sentence in doc.sents :
        res.append(sentence)
    return res




"""
path = "BSVV/2026 (en cours)"
df = df_create(path)

df = spacy_context_concat(df)
print(df)
"""