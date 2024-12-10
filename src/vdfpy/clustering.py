import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA


def cluster(df, method: str = "kmeans", n_clusters: int = 4):
    (n_samples, n_features) = df.shape

    print(
        f"# clusters: {n_clusters}; # samples: {n_samples}; # features {n_features}\n"
    )

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(data_scaled)

    if method == "kmeans":
        model = KMeans(
            init="k-means++", n_clusters=n_clusters, n_init=4, random_state=0
        )
        model.fit(df_scaled)
        labels = model.labels_
    elif method == "GMM":
        model = GaussianMixture(
            n_components=n_clusters, random_state=0, init_params="k-means++"
        ).fit(df_scaled)
        labels = model.predict(df_scaled)
    else:
        raise Exception(f"Clustering method {method} not implemented!")

    return labels
