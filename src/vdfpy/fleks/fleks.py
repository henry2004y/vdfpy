# FLEKS related methods

import pandas as pd
import flekspy as fl


def collect_moments(filename: str, preprocessed: bool = True) -> pd.DataFrame:
    ds = fl.load(filename)

    return