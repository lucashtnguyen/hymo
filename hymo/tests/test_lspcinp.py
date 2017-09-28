import os
import pytest
from io import StringIO

import pandas as pd
import pandas.util.testing as pdtest

from hymo import LSPCInpFile
from .utils import data_path

class base_LSPCInpFileMixin(object):
    def teardown(self):
        None

    def test_attributes(self):
        assert hasattr(self.inp, 'c70')
        assert isinstance(self.inp.c70, pd.DataFrame)
        assert hasattr(self.inp, 'c90')
        assert isinstance(self.inp.c90, pd.DataFrame)

class Test_LSPCInpFile(base_LSPCInpFileMixin):
    def setup(self):
        self.know_path = data_path(os.path.join('lspc', 'test_inp.inp'))
        self.c70_file = data_path(os.path.join('lspc', 'known_c70.csv'))
        self.c90_file = data_path(os.path.join('lspc', 'known_c90.csv'))

        self.inp = LSPCInpFile(self.know_path)

        self.known_c70_results = pd.read_csv(self.c70_file)
        self.known_c90_results = pd.read_csv(self.c90_file)

    def test_c90(self):
        pdtest.assert_frame_equal(
            self.inp.c90,
            self.known_c90_results
        )

    def test_c70(self):
        pdtest.assert_frame_equal(
            self.inp.c70,
            self.known_c70_results
        )