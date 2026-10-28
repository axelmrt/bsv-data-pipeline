import joblib
from sklearn.metrics import accuracy_score

from json_treatment import file_test,data_load


def accuracy(data_labeled_path : str, model_path : str) :
    """ Renvoie le score de précision de notre modèle IA sur un jeu de données étiquetter """
    data_labeled_path = file_test(data_labeled_path)

    test_vectors = data_load(data_labeled_path,"vector",context="test")
    test_labels = data_load(data_labeled_path,"label",context="test")

    model = joblib.load(model_path)
    predict_label = model.predict(test_vectors)
    return accuracy_score(test_labels,predict_label)


