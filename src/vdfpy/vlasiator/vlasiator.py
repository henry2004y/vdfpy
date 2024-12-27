# Vlasiator related methods

import pandas as pd
from pyvlasiator.vlsv import Vlsv
import numpy as np


def collect_moments(filename: str, preprocessed: bool = True) -> pd.DataFrame:
    ds = Vlsv(filename)
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
