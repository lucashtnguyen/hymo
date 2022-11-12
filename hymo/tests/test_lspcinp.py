import os
from io import StringIO

import pandas as pd
import pandas.util.testing as pdtest

from hymo import LSPCInpFile
from .utils import data_path


class base_LSPCInpFileMixin(object):
    def teardown(self):
        None

    def test_attributes(self):
        assert hasattr(self.inp, "c10")
        assert isinstance(self.inp.c10, pd.DataFrame)
        assert hasattr(self.inp, "c15")
        assert isinstance(self.inp.c15, pd.DataFrame)
        assert hasattr(self.inp, "c60")
        assert isinstance(self.inp.c60, pd.DataFrame)
        assert hasattr(self.inp, "c70")
        assert isinstance(self.inp.c70, pd.DataFrame)
        assert hasattr(self.inp, "c90")
        assert isinstance(self.inp.c90, pd.DataFrame)


class Test_LSPCInpFile(base_LSPCInpFileMixin):
    def setup(self):
        self.know_path = data_path(os.path.join("lspc", "test_inp.inp"))
        self.c70_file = data_path(os.path.join("lspc", "known_c70.csv"))
        self.c90_file = data_path(os.path.join("lspc", "known_c90.csv"))

        self.inp = LSPCInpFile(self.know_path)

        self.known_c70_results = pd.read_csv(self.c70_file)
        self.known_c90_results = pd.read_csv(self.c90_file)

    def test_c10(self):
        assert set(self.inp.c10.columns) == set(
            ["wfileid", "wfilename", "wparamnum", "wparamid1",]
        )
        assert len(self.inp.c10) == 15

    def test_c15(self):
        assert set(self.inp.c15.columns) == set(
            ["wstationid", "wfilenum", "wfileid1", "wfileid2"]
        )
        assert len(self.inp.c15) == 15

    def test_c60(self):
        assert set(self.inp.c60.columns) == set(
            ["subbasin", "defid", "nwst", "wst1", "wt1"]
        )
        assert len(self.inp.c60) == 17

    def test_c90(self):
        pdtest.assert_frame_equal(self.inp.c90, self.known_c90_results)

    def test_c70(self):
        pdtest.assert_frame_equal(self.inp.c70, self.known_c70_results)
