import os
from google import genai
from preprocess import df_create
from utilities import list_to_csv, file_is_empty,csv_to_list

#Variable globale pour l'IAG
client = genai.Client() #Import de la clé API notamment

# Le Prompt
alert_prompt = f"""
Tu es un expert agricole. Évalue le niveau d'alerte pour chaque observation de vigne ci-dessous.

Utilise strictement cette échelle numérique :
0 = Alerte Faible (Sain ou symptômes très légers sans danger immédiat)
1 = Alerte Moyenne (Début de maladie, vigilance requise)
2 = Alerte Élevée (Urgence, maladie grave ou propagation active)

Réponds UNIQUEMENT sous la forme d'une liste au format 'code_alerte', avec une ligne par observation. 
Ne saisis aucun autre texte, introduction ou explication.

Observations :"""

def labeling(data : list[str], prompt : str = alert_prompt, saved_file : str = "data_label.csv") -> list[int] :
    """Classifie les données dans des catégories grace a l'IAG et sauvegarde le tout dans un fichier csv"""
    if file_is_empty(saved_file) :
        labels = []
        data_formate = "\n".join([f"[{i}] {texte}" for i, texte in enumerate(data)])
        prompt = prompt + "\n" + data_formate
        #Demande a Gemini les etiquettes
        response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt,)
        for t in response.text.split("\n") :
            labels.append(int(t.strip()))
        list_to_csv(saved_file,data,labels)   #Sauvegarde dans un fichier csv
    else :
        # On part du principe que notre dernière colonne du fichier et les labels
        labels = csv_to_list(saved_file)[:,-1]
    return labels


    


