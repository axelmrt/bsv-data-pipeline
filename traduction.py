import csv
import json
import numpy as np
from vectorizer import tfidf


def csv_to_json(input_path : str , output_path : str,title : str ="Classification") -> None :
    #Ouvrir le fichier csv 
    encodings = ["utf-8", "latin-1", "iso-8859-1"]
    last_err = None
    mat = []
    for enc in encodings :
        try :
            with open(input_path, mode="r", newline="", encoding=enc) as f:
                reader = csv.reader(f)
                for row in reader :
                    mat.append(row)
                break
        except Exception as e :
            last_err = e
            mat = []
            if (enc == encodings[-1]) :
                print(f"Erreur durant l'ouverture du fichier {input_path} : {last_err}")
    #Construire le dictionnaire associé
    mat = np.array(mat)
    texts = mat[:,0]
    vectors = tfidf(texts)
    dict = {"metadata" : {"project" : title, 
                          "created_at": "2026-07-22",
                          "vectorizer_model": "tfidf",
                          "vector_dimension":len(vectors[0]),
                          "labels" : None,
                          "model" : None},
                          "samples" : []}
    #Gestion des csv sans label
    try :
        labels = mat[:,1]
        dict["metadata"]["labels"] = sorted(list(set(labels)))
    except IndexError as _ :
        labels = None

    #Remplissage des cases de texte et leurs informations
    for i in range(len(texts)):
        dict["samples"].append({"id": i, "text": texts[i],"vector":vectors[i].tolist(),
        "cat": labels[i] if labels is not None else None,
        "label": dict["metadata"]["labels"].index(labels[i]) if labels is not None else None,   #l'identifiant associé est sa position dans la liste
        "split": "test",
        "source": None})
    #Sauvegarder dans un fichier json
    with open(output_path,mode="w",encoding="utf-8") as f:
        json.dump(dict,f,indent=4, ensure_ascii=False)

def list_to_csv(nom_fichier : str , *colonnes : list) -> None:
    """Met les colonnes en paramètres dans un fichier csv"""
    tailles = np.array([len(c) for c in colonnes])
    if not colonnes :
        return 
    elif not np.all(tailles == np.max(tailles)) :
        print("Colonnes de tailles différentes")
        return 

    mat = np.column_stack(colonnes)
    with open(nom_fichier, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(mat)

def csv_to_list(nom_fichier : str) -> np.array :
    """Renvoie la matrice associé au fichier csv"""
    encodings = ["utf-8", "latin-1", "iso-8859-1"]
    last_err = []
    for enc in encodings :
        try :
            mat = []
            with open(nom_fichier, mode="r", newline="", encoding=enc) as f:
                reader = csv.reader(f)
                for row in reader :
                    mat.append(row)
            return np.array(mat)
        except Exception as e :
            last_err = e
            continue
    print(f"Erreur durant l'ouverture du fichier {nom_fichier} : {last_err}")
