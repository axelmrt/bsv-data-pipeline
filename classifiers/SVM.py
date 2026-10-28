import joblib

from sklearn.model_selection import train_test_split
# Algorithme de classification
from sklearn.svm import SVC                         # Support Vector Classifier

from sklearn.metrics import accuracy_score

from json_treatment import data_load,file_test,data_save,train_modif
#from traduction import csv_to_json



def SVM_train(input_path: str, model_path : str = "models/SVM.joblib", test_size: float = 0.2
               ,kernel : str = 'rbf' , C : float = 1.0 , gamma : str | float = 'scale') -> float | None:
    """ Entraine un modèle de Support Vector Machines et le sauvegarde"""
    # Data loading
    input_path = file_test(input_path)

    #Recuperation des vecteurs et labels
    vectors = data_load(input_path,"vector")
    labels = data_load(input_path,"label")
        

    # Répartition des données de test et d'entrainement
    if test_size > 0 :
        X_train, X_test, y_train, y_test = train_test_split(vectors, labels, test_size = test_size, random_state=42)
    else :
        X_train, X_test, y_train, y_test = vectors, vectors, labels, labels
    train_modif(input_path,X_train,model_path) #Enregistrement des données dans JSON qui servent d'entrainement

    # Entrainement du modèle et sauvegarde
    model = SVC(kernel = kernel,C = C,gamma = gamma)
    model.fit(X_train, y_train)
    joblib.dump(model,model_path)


    # Test du modèle : Accuracy
    if test_size > 0 and len(X_test) > 0 :
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy
    return None
    
def predict(input_path : str, model_path :str = "models/SVM.joblib") -> None :
    """ Prédit grace a un modèle de Support Vector Machines et sauvegarde dans un fichier CSV"""
    # Data loading
    input_path = file_test(input_path)

    #Recuperation des vecteurs et labels
    vectors = data_load(input_path,"vector")
    labels = data_load(input_path,"label")

    # Model loading
    model = joblib.load(model_path)

    # Prediction and save
    labels = model.predict(vectors)
    data_save(input_path,labels,"label")

