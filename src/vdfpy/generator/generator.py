# Pseudo distribution function generator.

import numpy as np
import pandas as pd


def make_clusters(
    n_samples: int = 10,
    n_clusters: int = 2,
    n_points: int = 100,
    n_dims: int = 1,
    *,
    random_state: int = None
) -> pd.DataFrame:
    """Create pseudo-distribution samples for testing the clustering methods.

    Args:
        n_samples (int, optional): Number of samples. Defaults to 10.
        n_clusters (int, optional): Number of clusters. Defaults to 2.
        n_points (int, optional): Number of maximum particles in each sampling. Defaults to 100.
        n_dims (int, optional): Dimensionality. Defaults to 1.
        random_state (int, optional): Seed for the random number generator. Defaults to None.

    Returns:
        pd.DataFrame: Samples of pseudo-distributions.
    """
    if random_state is not None:
        rng = np.random.default_rng(random_state)
    else:
        rng = np.random.default_rng()

    if n_dims == 1:
        upper = rng.integers(1, n_points, size=n_samples)
        if n_clusters == 1:
            samples = [rng.normal(0, 1, size=u) for u in upper]
        elif n_clusters == 2:
            ns2 = int(n_samples * 0.5)
            ns1 = n_samples - ns2
            s1 = [rng.normal(0, 1, size=upper[i]) for i in range(ns1)]
            s21 = [rng.normal(0, 1, size=upper[i]) for i in range(ns2, n_samples)]
            # Add bump-on-tail species
            s22 = [rng.normal(4, 1, size=upper[i] // 2) for i in range(ns2, n_samples)]
            s2 = [np.concatenate([arr1, arr2]) for arr1, arr2 in zip(s21, s22)]
            samples = s1 + s2
        elif n_clusters == 3:
            ns2 = int(n_samples / 3 * 2)
            ns1 = int(n_samples / 3)
            s1 = [rng.normal(0, 1, size=upper[i]) for i in range(ns1)]
            s21 = [rng.normal(0, 1, size=upper[i]) for i in range(ns1, ns2)]
            s22 = [rng.normal(4, 1, size=upper[i] // 2) for i in range(ns1, ns2)]
            s2 = [np.concatenate([arr1, arr2]) for arr1, arr2 in zip(s21, s22)]
            s31 = [rng.normal(0, 1, size=upper[i]) for i in range(ns2, n_samples)]
            s32 = [rng.normal(-4, 1, size=upper[i] // 2) for i in range(ns2, n_samples)]
            s3 = [np.concatenate([arr1, arr2]) for arr1, arr2 in zip(s31, s32)]
            samples = s1 + s2 + s3

        d1 = pd.Series(list(samples), name="particle velocity")
        d2 = pd.Series([float(s.shape[0]) for s in samples], name="density")
        d3 = pd.Series([np.mean(s) for s in samples], name="bulk velocity")
        d4 = pd.Series([np.std(s) for s in samples], name="temperature")
        df = pd.concat([d1, d2, d3, d4], axis=1)
    elif n_dims == 2:
        #TODO Complete the 2D generations!
        if n_clusters == 2:
            mean = [0, 0]
            cov = [[1, 0], [0, 1]]
            n1 = n_points
            samples1 = rng.multivariate_normal(mean, cov, size=n1)

            mean = [3, 3]
            cov = [[1, 0], [0, 1]]
            n2 = n_points // 10
            samples2 = rng.multivariate_normal(mean, cov, size=n2)

            samples = np.concatenate((samples1, samples2))

        df = pd.DataFrame(samples, columns=["x", "y"])

    return df
