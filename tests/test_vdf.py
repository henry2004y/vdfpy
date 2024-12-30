import pytest
import requests
import tarfile
import os

from flekspy.util import download_testfile

import vdfpy
import vdfpy.generator

filedir = os.path.dirname(__file__)

# Load Vlasiator test data
if os.path.isfile(filedir + "/data_vlasiator/bulk.1d.vlsv"):
    pass
else:
    url = (
        "https://raw.githubusercontent.com/henry2004y/vlsv_data/master/testdata.tar.gz"
    )
    testfiles = url.rsplit("/", 1)[1]
    r = requests.get(url, allow_redirects=True)
    open(testfiles, "wb").write(r.content)

    path = filedir + "/data_vlasiator"

    if not os.path.exists(path):
        os.makedirs(path)

    with tarfile.open(testfiles) as file:
        file.extractall(path)
    os.remove(testfiles)

# Load FLEKS test data
if os.path.isfile(filedir + "/data_fleks/Header"):
    pass
else:
    url = "https://raw.githubusercontent.com/henry2004y/batsrus_data/master/3d_particle.tar.gz"
    download_testfile(url, "tests/data_fleks")

class TestGenerator:
    def test_generate1d(self):
        df = vdfpy.generator.make_clusters()
        assert df.shape == (10, 5)
        df = vdfpy.generator.make_clusters(n_clusters=1, n_samples=1)
        assert df.shape == (1, 5)
        df = vdfpy.generator.make_clusters(
            n_clusters=3, n_points=2, n_samples=3, random_state=1
        )
        assert df["density"][0] == 1.0

    def test_generate2d(self):
        df = vdfpy.generator.make_clusters(
            n_clusters=2, n_dims=2, n_points=10, n_samples=3
        )
        assert df.shape == (3, 5)
        df = vdfpy.generator.make_clusters(
            n_clusters=1, n_dims=2, n_points=10, n_samples=2
        )
        assert df.shape == (2, 5)


class TestVlasiator:
    dir = "tests/data_vlasiator/"
    files = (dir + "bulk.1d.vlsv", dir + "bulk.2d.vlsv")

    def test_clustering(self):
        df = vdfpy.collect_moments(self.files[0])
        # default kmeans++
        labels = vdfpy.cluster(df, n_clusters=2)
        assert sum(labels) == 7
        labels = vdfpy.cluster(df, n_clusters=2, method="GMM")
        assert sum(labels) == 6

    def test_method_error(self):
        with pytest.raises(Exception):
            df = vdfpy.collect_moments(self.files[0])
            labels = vdfpy.cluster(df, method="none")


class TestFLEKS:
    dir = "tests/data_fleks/"
    file = dir + "3d_*amrex"

    def test_load(self):
        df = vdfpy.fleks.load(self.file)
        assert df.shape == (1,4)
