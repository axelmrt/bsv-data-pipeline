from classifiers.Spacy import SpacyModel
from classifiers.Textblob import TextBlobModel
from classifiers.SVM import SVM_train
from classifiers.Kmeans import Kmeans_clusters
from preprocess import df_create

from metrics import accuracy


############################ IA ###########################
labeled_file = "data/descriptions.csv"

#Utilisation du Spacy Model
model = SpacyModel()
Spacy_acc = model.train(labeled_file)
model.save("models/Spacy")
print(f"Précision du modèle Spacy : {Spacy_acc:.2f}")

#Utilisation du TextBlob Model (Naive Bayes Classifiers)
model = TextBlobModel()
Tb_acc = model.train(labeled_file)
model.save("models/Textblob.joblib")
print(f"Précision du modèle TextBlob (Naive Bayes Classifier) : {Tb_acc:.2f}")

#Utilisation du SVM Model
SVM_train(labeled_file)
SVM_acc = accuracy(labeled_file,"models/SVM.joblib")
print(f"Précision du modèle SVM : {SVM_acc:.2f}")

#Utilisation du K_means Model
Kmeans_sil = Kmeans_clusters(labeled_file)
print(f"Précision du modèle Kmeans : {Kmeans_sil:.2f}")


############################### BSV ###############################
bsv = "BSVV"
#Titres récupérés
data = df_create(bsv)
print(data.columns)