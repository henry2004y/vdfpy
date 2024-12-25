"""
vdfpy Public API.
"""

from .clustering import cluster

import numpy as np
import pandas as pd

from pyvlasiator.vlsv import Vlsv
import flekspy as fleks


def collect_moments(filename: str, preprocessed: bool = True) -> pd.DataFrame:
    """_summary_

    Args:
        filename (str): Input file name.
        preprocessed (bool, optional): Whether to use moments output directly. Defaults to True.

    Raises:
        NameError: If the file name is not recognized.

    Returns:
        pd.DataFrame: Pandas DataFrame for storing moments.
    """
    if filename.endswith(".vlsv"):  # Vlasiator
        ds = Vlsv(filename)
    elif filename.endswith(".out") or "amrex" in filename:  # FLEKS
        ds = fleks.load(filename)
    else:
        raise NameError("Unknown file type!")

    if preprocessed:
        feature = {}
        feature["n"] = ds.read_variable("proton/vg_rho")
        v = ds.read_variable("proton/vg_v")
        feature["v"] = np.linalg.norm(np.asarray(v), axis=-1)
        v = ds.read_variable("proton/vg_ptensor_diagonal")
        feature["p"] = np.mean(v, axis=-1)

        df = pd.DataFrame(feature)
    else:
        ds.init_cellswithVDF("proton")
        cVDF = ds.meshes["proton"].cellwithVDF

        data = []

        for i, cid in enumerate(cVDF):
            feature = {}
            feature["n"] = ds.read_variable("proton/vg_rho", cid)
            v = ds.read_variable("proton/vg_v", cid)
            feature["v"] = np.linalg.norm(np.asarray(v), axis=-1)
            v = ds.read_variable("proton/vg_ptensor_diagonal", cid)
            feature["p"] = np.mean(v, axis=-1)

            data.append(feature)

        df = pd.DataFrame(data)

    return df


def load_mms(filename: str):
    print("TBD!")
