import pytest
import requests
import tarfile
import os

import vdfpy
import vdfpy.generator

filedir = os.path.dirname(__file__)

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


class TestGenerator:
    def test_generate(self):
        df = vdfpy.generator.make_clusters()
        assert df.shape == (10, 4)


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
