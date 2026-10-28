import numpy as np
import csv 
import json
import pandas as pd


def load_data(nom_fichier : str) -> pd.DataFrame | list | dict :
    """Reconnait la fichier d'entrée et renvoie sa structure de données associé. JSON -> Dict, CSV ->List/Dataframe."""
    pass

def save_data(data : pd.DataFrame | list | dict) -> None :
    """Reconnait la donnée d'entrée et la sauvegarde dans son fichier associé"""
    pass

def dataframe_to_csv(nom_fichier : str, df : pd.DataFrame) -> None :
    """Prend toutes les colonnes du Dataframe et les enregistre dans un fichier csv"""
    columns = df.columns()
    
    pass



def stop_words(nom_fichier : str) -> list :
    """ Ouvre et enregistre les stop_words du fichier"""
    with open(nom_fichier,mode="r", encoding="utf-8") as f :
        liste = json.load(f)
    return liste

def file_is_empty(nom_fichier : str) -> bool :
    """Verifie si un fichier est vide"""
    with open(nom_fichier, 'r') as file:
        content = file.read()
        if len(content) == 0:
            return True
        else:
            return False

# JSON loading and saving
def json_load(path : str) -> dict[str,any] :
    """ Renvoie le contenue d'un fichier JSON """
    encodings = ["utf-8", "latin-1", "iso-8859-1"]
    for enc in encodings :
        try :
            with open(path,mode="r", encoding=enc) as f :
                dict = json.load(f)
            return dict
        except Exception as e :
            last_err = e
            if (enc == encodings[-1]) :
                raise Exception(f"Erreur durant l'ouverture du fichier {path} : {last_err}")

def json_save(path:str, data : any) -> None:
    """ Sauvegarde le contenu dans le fichier JSON donner en paramètres """
    try :
        with open(path,mode="w",encoding="utf-8") as f:
            json.dump(data,f,indent=4, ensure_ascii=False)
    except Exception as e :
        print(f"Erreur durant l'ouverture du fichier {path} : {e}")