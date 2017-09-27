import os
import pytest
from io import StringIO

import pandas as pd
import pandas.util.testing as pdtest

from hymo import LSPCInpFile
from .utils import data_path

class Test_LSPCInp(object):
    def setup(self):
        self. know_path = data_path(os.path.join('lspc', 'known_inp.inp'))
        self.inp = LSPCInpFile(self.know_path)

    def teardown(self):
        None

    def test_attributes(self):
        assert hasattr(self.inp, 'c70')
        assert hasattr(self.inp, 'c90')
        # assert isinstance(self.inp.title, pd.DataFrame)