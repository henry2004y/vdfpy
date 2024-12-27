# FLEKS related methods

import pandas as pd
import numpy as np
import flekspy as fl


def load(filename: str, left_edge=None, right_edge=None) -> pd.DataFrame:
    """Return a dataframe from FLEKS particle data.

    Args:
        filename (str): FLEKS output file directory.
        left_edge: box left edges for the selected particles. If None, choose the whole domain.
        right_edge: box left edges for the selected particles. If None, choose the whole domain.

    Returns:
        A pandas DataFrame with 2D particle raw data and moments.
    """
    ds = fl.load(filename)
    if left_edge is None:
        left_edge = ds.domain_left_edge
    if right_edge is None: 
        right_edge = ds.domain_right_edge
    box = ds.box(left_edge=left_edge, right_edge=right_edge)
    vx = box["particle_velocity_x"].to_ndarray()
    vy = box["particle_velocity_y"].to_ndarray()
    v = {"vx": vx, "vy": vy}
    samples = [pd.DataFrame(v)]
    d1 = pd.Series(samples, name="particle velocity")
    d2 = pd.Series([float(s.shape[0]) for s in samples], name="density")
    d3 = pd.Series([np.mean(s, axis=0) for s in samples], name="bulk velocity")
    # scalar temperature
    d4 = pd.Series([np.mean(np.std(s, axis=0)) for s in samples], name="temperature")
    df = pd.concat([d1, d2, d3, d4], axis=1)

    return df


def collect_moments(filename: str, preprocessed: bool = True) -> pd.DataFrame:
    ds = fl.load(filename)

    return
