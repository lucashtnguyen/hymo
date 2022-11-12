import os

import pandas as pd

from hymo import SWMMInterfaceFile
from .utils import data_path


class base_SWMMInterfaceFileMixin(object):

    def teardown(self):
        None

    def test_attributes(self):

        assert hasattr(self.interface, 'interface')
        assert isinstance(self.interface.interface, pd.DataFrame)

        assert hasattr(self.interface, 'header')
        assert isinstance(self.interface.header, str)

        assert hasattr(self.interface, 'units')
        assert isinstance(self.interface.units, dict)

        assert hasattr(self.interface, 'nodes')
        assert isinstance(self.interface.nodes, list)

    def test_nodes(self):
        assert self.interface.nodes == ['OF-1', 'INF-BR']
        assert len(self.interface.nodes) == 2

    def test_units(self):
        assert self.interface.units == {
            'water': 'MG/L', 'FLOW': 'CFS', 'nitrogen': 'MG/L'}
        assert len(self.interface.units) == 3

    def test_interface(self):
        header_length = len(self.interface.header.splitlines())

        assert len(self.interface.interface) + \
            1 == len(self.interface.orig_file) - header_length


class Test_SWMMInterfaceFile(base_SWMMInterfaceFileMixin):

    def setup(self):
        self.known_path = data_path(os.path.join('swmm', 'test_interface.txt'))
        self.interface = SWMMInterfaceFile(self.known_path)
