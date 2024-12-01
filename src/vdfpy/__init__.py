"""
vdfpy Public API.
"""

from .clustering import (
    cluster
)

import os
import sys
import glob
import numpy as np
import pandas as pd
import scipy.stats as scs

from pyvlasiator.vlsv import Vlsv
import flekspy as fleks

# import matplotlib as mpl
# import matplotlib.pyplot as plt


def collect_moments(filename: str):
    if filename.endswith(".vlsv"):  # Vlasiator
        ds = Vlsv(filename)
    elif filename.endswith(".out") or "amrex" in filename:  # FLEKS
        ds = fleks.load(filename)
    else:
        raise NameError("Unknown file type!")

    ds.init_cellswithVDF("proton")
    cVDF = ds.meshes["proton"].cellwithVDF

    data = []

    for i, cid in enumerate(cVDF):
        feature = {}
        feature["n"] = ds.read_variable("proton/vg_rho", cid)
        v = ds.read_variable("proton/vg_v", cid)
        feature["v"] = np.linalg.norm(np.asarray(v), axis=-1)
        v = ds.read_variable("proton/vg_ptensor_diagonal", cid)
        feature["p"] = np.average(v)

        data.append(feature)

    df = pd.DataFrame(data)

    return df

def load_mms(filename: str):
    print("TBD!")
