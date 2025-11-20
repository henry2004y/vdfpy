import numpy as np
import pytest
from sklearn.mixture import GaussianMixture
from unittest.mock import MagicMock

from vdfpy.generator import get_gmm_parameters


@pytest.fixture
def fitted_gmm():
    """Provides a mock fitted GaussianMixture object."""
    gmm = MagicMock(spec=GaussianMixture)
    gmm.n_components = 2
    gmm.means_ = np.array([[0.0, 1.0], [2.0, 3.0]])
    gmm.covariances_ = np.array([[[1.0, 0.5], [0.5, 2.0]], [[3.0, -0.2], [-0.2, 4.0]]])
    return gmm


def test_get_gmm_parameters_isotropic(fitted_gmm):
    """
    Tests the extraction of isotropic squared thermal velocities from a GMM.
    """
    parameters = get_gmm_parameters(fitted_gmm, isotropic=True)

    assert len(parameters) == 2
    # v_th_sq_1 = (1.0 + 2.0) / 2.0 = 1.5
    assert parameters[0]["v_th_sq"] == pytest.approx(1.5)
    # v_th_sq_2 = (3.0 + 4.0) / 2.0 = 3.5
    assert parameters[1]["v_th_sq"] == pytest.approx(3.5)


def test_get_gmm_parameters_bi_maxwellian(fitted_gmm):
    """
    Tests the extraction of Bi-Maxwellian squared thermal velocities from a GMM.
    """
    parameters = get_gmm_parameters(fitted_gmm, isotropic=False)

    assert len(parameters) == 2
    # v_parallel_sq_1 = 1.0
    assert parameters[0]["v_parallel_sq"] == pytest.approx(1.0)
    # v_perp_sq_1 = 2.0
    assert parameters[0]["v_perp_sq"] == pytest.approx(2.0)
    # v_parallel_sq_2 = 3.0
    assert parameters[1]["v_parallel_sq"] == pytest.approx(3.0)
    # v_perp_sq_2 = 4.0
    assert parameters[1]["v_perp_sq"] == pytest.approx(4.0)
