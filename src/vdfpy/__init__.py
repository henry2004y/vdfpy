"""
vdfpy Public API.
"""

from .clustering import cluster
import vdfpy.vlasiator as vlasiator
import vdfpy.fleks as fleks

import pandas as pd


def collect_moments(filename: str, preprocessed: bool = True) -> pd.DataFrame:
    """Collect plasma moments from data.

    Args:
        filename (str): Input file name.
        preprocessed (bool, optional): Whether to use moments output directly. Defaults to True.

    Raises:
        NameError: If the file name is not recognized.

    Returns:
        pd.DataFrame: Pandas DataFrame for storing moments.
    """
    if filename.endswith(".vlsv"):  # Vlasiator
        df = vlasiator.collect_moments(filename)
    elif filename.endswith(".out") or "amrex" in filename:  # FLEKS
        df = fleks.collect_moments(filename)
    else:
        raise NameError("Unknown file type!")

    return df


def load_mms(filename: str):
    print("TBD!")
