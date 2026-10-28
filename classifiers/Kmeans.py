from json_treatment import data_load,file_test

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def Kmeans_clusters(input_path : str,num_clusters : int = 3) -> float :
    """ A partir de données textuels les groupes de mots sont classés dans des clusters représentatifs """
    input_path = file_test(input_path)

    vectors = data_load(input_path,"vector")

    # Clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(vectors)
    return silhouette_score(vectors,clusters)