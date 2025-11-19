import numpy as np
from vdfpy.generator import sample_box_muller, sample_mcmc


def test_sample_box_muller():
    """Test the Box-Muller sampler."""
    rng = np.random.default_rng(0)
    n_particles = 10000
    bulk_velocity = 1.0
    temperature = 2.0
    velocities = sample_box_muller(
        n_particles, bulk_velocity, temperature, rng=rng
    )
    # Check the moments of the sampled distribution
    assert np.isclose(np.mean(velocities), bulk_velocity, atol=0.1)
    assert np.isclose(np.var(velocities), temperature, atol=0.1)


def test_sample_box_muller_3d():
    """Test the Box-Muller sampler in 3D."""
    rng = np.random.default_rng(0)
    n_particles = 10000
    bulk_velocity = 1.0
    temperature = 2.0
    n_dims = 3
    velocities = sample_box_muller(
        n_particles, bulk_velocity, temperature, n_dims=n_dims, rng=rng
    )
    # Check the moments of the sampled distribution
    assert np.all(np.isclose(np.mean(velocities, axis=0), bulk_velocity, atol=0.1))
    assert np.all(np.isclose(np.var(velocities, axis=0), temperature, atol=0.1))


def test_sample_mcmc():
    """Test the MCMC sampler."""
    rng = np.random.default_rng(0)
    # Define a custom log probability function (e.g., a standard normal distribution)
    def log_prob_func(x):
        return -0.5 * x**2

    n_particles = 1000
    initial_state = 0.0
    samples = sample_mcmc(
        n_particles, log_prob_func, initial_state, rng, burn_in=500
    )
    # Check the moments of the sampled distribution
    assert np.isclose(np.mean(samples), 0, atol=0.1)
    assert np.isclose(np.var(samples), 1, atol=0.1)


def test_sample_mcmc_3d():
    """Test the MCMC sampler in 3D."""
    rng = np.random.default_rng(0)
    # Define a custom log probability function (e.g., a standard normal distribution)
    def log_prob_func(x):
        return -0.5 * np.sum(x**2)

    n_particles = 5000
    n_dims = 3
    initial_state = np.zeros(n_dims)
    samples = sample_mcmc(
        n_particles,
        log_prob_func,
        initial_state,
        rng,
        n_dims=n_dims,
        proposal_width=0.5,
        burn_in=2000,
    )
    # Check the moments of the sampled distribution
    assert np.all(np.isclose(np.mean(samples, axis=0), 0, atol=0.1))
    assert np.all(np.isclose(np.var(samples, axis=0), 1, atol=0.2))
