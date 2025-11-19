# Pseudo distribution function generator.

import random
import math
import numpy as np
import pandas as pd


def make_clusters(
    n_samples: int = 10,
    n_clusters: int = 2,
    n_points: int = 100,
    n_dims: int = 1,
    *,
    random_state: int = None,
    shuffle: bool = False
) -> pd.DataFrame:
    """Create pseudo-distribution samples for testing the clustering methods.

    Args:
        n_samples (int, optional): Number of samples. Defaults to 10.
        n_clusters (int, optional): Number of clusters. Defaults to 2.
        n_points (int, optional): Number of maximum particles in each sampling. Defaults to 100.
        n_dims (int, optional): Dimensionality. Defaults to 1.
        random_state (int, optional): Seed for the random number generator. Defaults to None.
        shuffle (bool, optional): Shuffle the sampling order. Defaults to False.

    Returns:
        pd.DataFrame: Samples of pseudo-distributions.
    """
    assert n_samples >= n_clusters, "Cannot generate fewer samples than classes!"
    if random_state is not None:
        rng = np.random.default_rng(random_state)
    else:
        rng = np.random.default_rng()

    if n_dims == 1:
        upper = rng.integers(1, n_points, size=n_samples)
        if n_clusters == 1:
            samples = [rng.normal(0, 1, size=u) for u in upper]
            dclass = pd.Series(np.ones(n_samples, dtype=int), name="class")
        elif n_clusters == 2:
            ns1 = n_samples - math.ceil(n_samples / 2)
            s1 = [rng.normal(0, 1, size=upper[i]) for i in range(ns1)]
            s21 = [rng.normal(0, 1, size=upper[i]) for i in range(ns1, n_samples)]
            # Add bump-on-tail species
            s22 = [rng.normal(4, 1, size=upper[i] // 2) for i in range(ns1, n_samples)]
            s2 = [np.concatenate([arr1, arr2]) for arr1, arr2 in zip(s21, s22)]
            samples = s1 + s2
            dclass = pd.Series(
                np.concatenate(
                    (np.ones(ns1, dtype=int), np.full(n_samples - ns1, 2, dtype=int))
                ),
                name="class",
            )
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
            dclass = pd.Series(
                np.concatenate(
                    (
                        np.ones(ns1, dtype=int),
                        np.full(ns2 - ns1, 2, dtype=int),
                        np.full(n_samples - ns2, 3, dtype=int),
                    )
                ),
                name="class",
            )

        if shuffle:
            random.shuffle(samples)

        samples = [pd.DataFrame(s, columns=["vx"]) for s in samples]
        d1 = pd.Series(samples, name="particle velocity")
        d2 = pd.Series([float(s.shape[0]) for s in samples], name="density")
        d3 = pd.Series([np.mean(s) for s in samples], name="bulk velocity")
        d4 = pd.Series([np.std(s.values) for s in samples], name="temperature")
    elif n_dims == 2:
        upper = rng.integers(1, n_points, size=n_samples)
        if n_clusters == 1:
            mean = [0, 0]
            cov = [[1, 0], [0, 1]]
            samples = [rng.multivariate_normal(mean, cov, size=u) for u in upper]
            dclass = pd.Series(np.ones(n_samples, dtype=int), name="class")
        elif n_clusters == 2:
            ns1 = n_samples - math.ceil(n_samples / 2)

            mean1 = [0, 0]
            cov1 = [[1, 0], [0, 1]]
            s1 = [
                rng.multivariate_normal(mean1, cov1, size=upper[i]) for i in range(ns1)
            ]

            mean2 = [4, 4]
            cov2 = [[1, 0], [0, 1]]
            s21 = [
                rng.multivariate_normal(mean1, cov1, size=upper[i])
                for i in range(ns1, n_samples)
            ]
            s22 = [
                rng.multivariate_normal(mean2, cov2, size=upper[i] // 2)
                for i in range(ns1, n_samples)
            ]
            s2 = [np.concatenate([arr1, arr2]) for arr1, arr2 in zip(s21, s22)]

            samples = s1 + s2
            dclass = pd.Series(
                np.concatenate(
                    (np.ones(ns1, dtype=int), np.full(n_samples - ns1, 2, dtype=int))
                ),
                name="class",
            )

        if shuffle:
            random.shuffle(samples)

        samples = [pd.DataFrame(s, columns=["vx", "vy"]) for s in samples]
        d1 = pd.Series(samples, name="particle velocity")
        d2 = pd.Series([float(s.shape[0]) for s in samples], name="density")
        d3 = pd.Series([np.mean(s, axis=0) for s in samples], name="bulk velocity")
        # scalar temperature
        d4 = pd.Series(
            [np.mean(np.std(s, axis=0)) for s in samples], name="temperature"
        )

    df = pd.concat([dclass, d1, d2, d3, d4], axis=1)

    return df


def sample_box_muller(
    n_particles: int, bulk_velocity: float, temperature: float, *, rng: np.random.Generator = None
) -> np.ndarray:
    """Sample particles from a Maxwellian distribution using the Box-Muller method.
    Args:
        n_particles (int): Number of particles to sample.
        bulk_velocity (float): Bulk velocity of the distribution.
        temperature (float): Temperature of the distribution.
        rng (np.random.Generator, optional): Random number generator instance. Defaults to None.
    Returns:
        np.ndarray: Array of particle velocities.
    """
    if rng is None:
        rng = np.random.default_rng()

    # We need n_particles samples, Box-Muller generates pairs of samples.
    # So we generate ceil(n_particles / 2) pairs.
    num_pairs = (n_particles + 1) // 2
    u1 = rng.random(num_pairs)
    u2 = rng.random(num_pairs)

    # Box-Muller transform for standard normal
    r = np.sqrt(-2 * np.log(u1))
    theta = 2 * np.pi * u2
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Combine and truncate to get n_particles samples
    z = np.concatenate((x, y))[:n_particles]

    # Scale and shift to match the given moments
    sigma = np.sqrt(temperature)
    velocities = bulk_velocity + sigma * z
    return velocities


def sample_mcmc(
    n_particles: int,
    log_prob_func: callable,
    initial_state: float,
    rng: np.random.Generator,
    proposal_width: float = 1.0,
    burn_in: int = 100,
) -> np.ndarray:
    """Sample particles from a custom distribution using the MCMC method.
    Args:
        n_particles (int): Number of particles to sample.
        log_prob_func (callable): Function that computes the log probability of the distribution.
        initial_state (float): Initial state for the MCMC sampler.
        rng (np.random.Generator): Random number generator.
        proposal_width (float, optional): Width of the proposal distribution. Defaults to 1.0.
        burn_in (int, optional): Number of burn-in samples to discard. Defaults to 100.
    Returns:
        np.ndarray: Array of particle velocities.
    """
    # Initialize the MCMC chain
    total_samples = n_particles + burn_in
    chain = np.zeros(total_samples)
    chain[0] = initial_state
    log_prob_current = log_prob_func(initial_state)

    # Run the MCMC sampler
    for i in range(1, total_samples):
        # Propose a new state
        proposal = chain[i - 1] + rng.normal(0, proposal_width)
        # Compute the acceptance ratio
        log_prob_proposal = log_prob_func(proposal)
        log_acceptance_ratio = log_prob_proposal - log_prob_current
        # Accept or reject the proposal
        if np.log(rng.random()) < log_acceptance_ratio:
            chain[i] = proposal
            log_prob_current = log_prob_proposal
        else:
            chain[i] = chain[i - 1]

    return chain[burn_in:]
