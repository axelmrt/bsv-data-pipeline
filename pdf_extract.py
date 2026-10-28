import fitz  # PyMuPDF
import pymupdf
import re
import os
import numpy as np

def text_extract(pdf_path : str) -> str:
    doc = fitz.open(pdf_path)
    blocs_texte_globaux = []
    """
    # On retire les 15 dernières pages qui constitue l'annexe ajouté a chaque fin de BSV
    if len(doc) > 15 :
        page_BSV = len(doc) - 15 
        del doc[page_BSV:]       """    
    
    for page in doc:
        # Récupération des blocs de la page
        blocs = page.get_text("blocks")
        # Tri des blocs du haut vers le bas, puis de gauche à droite (sens de lecture)
        blocs.sort(key=lambda b: (b[1], b[0]))      # b[1] -> y0 , b[0] -> x0 

        for b in blocs:
            txt = b[4].strip()
            if txt:
                # Astuce de nettoyage : si un bloc se termine par un tiret de césure "-", 
                # on le nettoie pour la continuité du mot sur la page suivante
                blocs_texte_globaux.append(txt)
                
    # On fusionne TOUT le texte du PDF avec des sauts de ligne. 
    # Le document devient un seul flux continu de texte.
    return "\n".join(blocs_texte_globaux)


def paragraph_cut2(pdf_path : str) -> dict[str,str] :
    """Partitionne le texte en paragraphe en utilisant la typographie des titres"""
    doc = fitz.open(pdf_path)
    titres = []

    sections = {}
    nom_section_courante = "INTRODUCTION / EN-TÊTE"
    contenu_courant = []

    #Determination de la taille du corps du texte
    fontsize = []
    for page in doc :
        blocks = page.get_text("dict").get("blocks",[])
        for bloc in blocks :
            for line in bloc.get("lines",[]) :
                for span in line.get("spans",[]) :
                    fontsize.append(span.get("size", 0))    #Récupération des tailles de police d'écriture
    unique, counts = np.unique(np.array(fontsize),return_counts=True) 
    taille_texte = unique[np.argmax(counts)]    # Taille de police qui se répéte le plus

    for page in doc :
        blocks = page.get_text("dict").get("blocks",[])
        for bloc in blocks :
            for line in bloc.get("lines",[]) :
                #Plus d'information dans le span utile pour les filtrages typographiques
                for span in line.get("spans",[]) :
                    #Test si c'est un titre
                    text = span.get("text","").strip()
                    if not text :   #On Skip ce span s'il est vide
                        continue
                    color = pymupdf.sRGB_to_rgb(span.get("color",0))
                    #Filtrage des full majuscules
                    est_maj = re.match(r'^[A-ZÀ-ÖÙ-Ý\s\-\’\']+[A-Z0-9À-ÖÙ-Ý\s\-\’\']+$', text)
                    #Filtrage de la taille
                    est_taille_normal = 3 <= len(text) <= 40
                    #Filtrage par expression régulière d'une adresse mail
                    est_mail = re.match(r"([a-z0-9\;\_\-\.]+@[a-z0-9\;\_\-\.]+.[a-z0-9\;\_\-]+)",text) 
                    #Filtrage par expression régulière d'un URL avec protocole http/https
                    est_lien = re.match(r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,63}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$",text)
                    #Filtrage des termes d'une autre couleurs que Noir ou blanc
                    est_colorée = (color != (0,0,0)) and (color != (255,255,255)) and (text != "")
                    #Filtrage des termes en gras
                    est_en_gras = (span.get("flags", 0) == 16) and (text != "")
                    #Filtrage d'une taille supérieur a celle du corps du texte
                    est_plus_grands_corps_texte = (span.get("size",0) > taille_texte) and (text != "")
                    #Filtrage des titres
                    est_titre = est_en_gras and est_colorée and est_plus_grands_corps_texte and est_maj and est_taille_normal and not est_lien and not est_mail
                    if est_titre :
                        # On sauvegarde la section qui vient de se terminer 
                        sections[nom_section_courante] = "\n".join(contenu_courant).strip()
                        nom_section_courante = text
                        contenu_courant = []
                    else:
                        contenu_courant.append(text)
    return sections

def paragraph_cut(pdf_path : str) -> dict[str,str]:
    """Partitionne le texte en paragraphe en partant du principe que chaque
    paragraphe commence par un titre tout en Majuscule"""
    # On récupère l'intégralité du document en un seul bloc textuel
    texte_entier = text_extract(pdf_path)
    
    sections = {}
    nom_section_courante = "INTRODUCTION / EN-TÊTE"
    contenu_courant = []
    
    lignes = texte_entier.split('\n')
    
    for ligne in lignes:
        ligne_clean = ligne.strip()
        # Pas de texte on passe a la ligne d'après
        if not ligne_clean:
            continue
            
        # Détection des titres (Ligne en majuscules, entre 3 et 40 caractères, ne peut pas commencer par un chiffre)
        est_un_titre = re.match(r'^[A-ZÀ-ÖÙ-Ý\s\-\’\']+[A-Z0-9À-ÖÙ-Ý\s\-\’\']+$', ligne_clean) and 3 <= len(ligne_clean) <= 40
        
        # Filtrer les en-têtes/pieds de page qui reviennent sur chaque page en majuscules
        exclusions = ["BULLETIN DE SANTÉ DU VÉGÉTAL", "CHAMBRES D'AGRICULTURE", "VITICULTURE"]
        # not any exclu la présence d'exclusion dans ligne_clean
        est_un_titre = est_un_titre and not any(ex in ligne_clean for ex in exclusions)

        if est_un_titre:
            # On sauvegarde la section qui vient de se terminer 
            sections[nom_section_courante] = "\n".join(contenu_courant).strip()
            nom_section_courante = ligne_clean
            contenu_courant = []
            
        else:
            contenu_courant.append(ligne)
            
    # Sauvegarde de la dernière section
    sections[nom_section_courante] = "\n".join(contenu_courant).strip()

    # Pour chaque paragraphe on modifie le contenu pour avoir un texte linéaire
    titles = sections.keys()
    for title in titles :
        sections[title] = re.sub(r"\s+", " ", sections[title]) #N'importe quelle de saut est remplacé par un espace
    return sections

def safe_base_dir():
    """Utile à connaitre le chemin du fichier exécuté"""
    # si __file__ n'existe pas (ex: execution interactive), fallback sur cwd
    return os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()

BASE_DIR = safe_base_dir()

def repertory_extract(repertory_path : str) -> dict[dict[str,str],str] :
    """Renvoie un dictionnaire avec le texte partitionner (dans un dictionnaire)
       et son nom de fichier associé."""
    
    all_docs = {}
    path = BASE_DIR + "/" + repertory_path

    try :
        for racine, dossiers, fichiers in os.walk(path):
            #On parcours recursivement tout le fichier
            #print(f"Dans le dossier : {racine}")
            for nom in fichiers:
                # On ne regarde que les fichier pdf
                is_pdf = nom.endswith(".pdf")
                if is_pdf :
                    path_to_doc = racine + "/" + nom
                    document_text = paragraph_cut(path_to_doc)
                    all_docs[nom] = document_text
                    #print(f"Fichier PDF : {nom}")
                #else :
                    #print(f"Fichier : {nom}")
            #for nom in dossiers:
                #print(f"Sous-dossier : {nom}") 
    except Exception as e:
        print(f"Erreur fichier inconnue'{path}': {e}")
        return 
    return all_docs

"""
pdf_path = "/home/axel/Stage/BSV/BSVV/bsvviti_20260519_n10.pdf"
print(paragraph_cut(pdf_path))
print(paragraph_cut2(pdf_path))
"""
"""
rep_path = "BSVV"
repertory_extract(rep_path) """
