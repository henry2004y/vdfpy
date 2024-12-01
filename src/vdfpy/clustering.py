import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def cluster(df, method: str = "kmeans"):
    (n_samples, n_features) = df.shape
    n_clusters = 4

    print(
        f"# clusters: {n_clusters}; # samples: {n_samples}; # features {n_features}\n"
    )

    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(data_scaled)

    kmeans = KMeans(init="k-means++", n_clusters=n_clusters, n_init=4, random_state=0)
    kmeans.fit(df_scaled)

    return kmeans.labels_
