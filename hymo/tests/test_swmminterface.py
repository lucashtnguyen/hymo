import os

import pandas as pd

from hymo import SWMMInterfaceFile
from .utils import data_path


class base_SWMMInterfaceFileMixin(object):

    def teardown_method(self):
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

    def test_interface_shape_columns_and_boundary_rows(self):
        df = self.interface.interface

        assert df.shape == (960, 11)
        assert df.columns.tolist() == [
            "Node",
            "Year",
            "Mon",
            "Day",
            "Hr",
            "Min",
            "Sec",
            "FLOW",
            "water",
            "nitrogen",
            "",
        ]
        assert df.iloc[0].loc[["Node", "Year", "Mon", "Day", "Hr", "Min"]].to_dict() == {
            "Node": "OF-1",
            "Year": 2016,
            "Mon": 1,
            "Day": 1,
            "Hr": 0,
            "Min": 0,
        }
        assert df.iloc[-1].loc[["Node", "Day", "Hr", "Min", "FLOW"]].to_dict() == {
            "Node": "INF-BR",
            "Day": 5,
            "Hr": 23,
            "Min": 45,
            "FLOW": 0.0,
        }


class Test_SWMMInterfaceFile(base_SWMMInterfaceFileMixin):

    def setup_method(self):
        self.known_path = data_path(os.path.join('swmm', 'test_interface.txt'))
        self.interface = SWMMInterfaceFile(self.known_path)
