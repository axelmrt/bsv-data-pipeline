from utilities import json_save,json_load
from typing import Literal

from traduction import csv_to_json

#Fonction permettant l'acceptation de fichier csv simple
def file_test(path : str) -> str :
    if path.endswith(".csv") :
        ancient_path = path
        path = path[0:-4] + ".json"
        csv_to_json(ancient_path,path)
    elif not path.endswith(".json") :
        raise Exception(f"Mauvais fichier d'entrée {path}")
    return path

# Data load from json
def metadata_load(path : str, data_type : Literal["model","labels"]) -> str :
    dict = json_load(path)
    output = dict["metadata"][data_type]
    if output is None and data_type == "model" :
        raise ValueError(f"{path}")
    else :
        return output

def data_load(path : str,data_type : Literal["vector", "label", "text", "source","cat"],
              context : Literal["test","train"] | None = None) -> list :
    """ Renvoie la donnée demander pour chaque élement du fichier sous forme de liste"""
    dict = json_load(path)
    samples = dict["samples"]
    taille = len(samples)
    var = []
    for i in range(taille):
        var.append(samples[i][data_type])
    if context is not None :
        context_var = []
        for i in range(len(var)) :
            if samples[i]["split"] == context :
                context_var.append(var[i])
        output = context_var
        if not output :
            raise ValueError(f"Pas de données {context} dans {path}")
    else :
        output = var
    return output


# Modification du JSON
def train_modif(path: str,trainer_vectors : list[list[float]],model : str | None = None)-> None :
    """ Enregistre dans le JSON les données qui ont servis d'entrainement au modèle et son emplacement"""
    dict = json_load(path)
    vectors = data_load(path,"vector")
    #Recuperation des indices des données d'entrainement (Donc ne pouvant pas tester la performance du modèle)
    ind = []
    for i,v in enumerate(vectors):
        for u in trainer_vectors :
            if u == v :
                ind.append(i)

    #Enregistrement des données
    dict["metadata"]["model"] = model   #Sauvegarde de l'emplacement du modèle entrainé
    for i in ind :
        dict["samples"][i]["split"] = "train"
    json_save(path,dict)

def data_save(path:str,data : list,data_type : Literal["vector", "label", "text","split", "source"]) -> None :
    """ Ajoute les données données dans le fichier JSON """
    # Test a ajouté : vérifier correspondance type de la data et data_type
    # Vérifier que data est la meme taille que dict["samples"]
    dict = json_load(path)
    for i in range(len(dict["samples"])):
        dict["samples"][i][data_type] = data[i]
    json_save(path,dict)

def data_add(path : str , text : str, ) :
    """ Ajoute un élément de texte et ces données a notre fichier JSON """
    pass

# Test du statut du json
def statut(path : str, search : Literal["vectorized","labelled","trained"]) -> bool :
    """ Test la situation du JSON """
    if search == "vectorized" :
        return not any(v is None for v in data_load(path,"vector"))
    elif search == "labelled" :
        return not any(v is None for v in data_load(path,"label"))
    elif search == "trained" :
        return not metadata_load(path,"model") is None



    


