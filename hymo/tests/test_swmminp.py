import os
import pytest
from pkg_resources import resource_filename

import pytest
import pandas as pd
import pandas.util.testing as pdtest

from hymo import SWMMInpFile
from .utils import data_path

class base_SWMMInpFileMixin(object):
    def teardown(self):
        None

    def test_attributes(self):
        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'title')
            assert isinstance(self.inp.title, pd.DataFrame)

        assert hasattr(self.inp, 'options')
        assert isinstance(self.inp.options, pd.DataFrame)

        assert hasattr(self.inp, 'evaporation')
        assert isinstance(self.inp.evaporation, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'temperature')
            assert isinstance(self.inp.temperature, pd.DataFrame)

        assert hasattr(self.inp, 'raingages')
        assert isinstance(self.inp.raingages, pd.DataFrame)

        assert hasattr(self.inp, 'subcatchments')
        assert isinstance(self.inp.subcatchments, pd.DataFrame)

        assert hasattr(self.inp, 'subareas')
        assert isinstance(self.inp.subareas, pd.DataFrame)

        assert hasattr(self.inp, 'infiltration')
        assert isinstance(self.inp.infiltration, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'lid_controls')
            assert isinstance(self.inp.lid_controls, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'lid_usage')
            assert isinstance(self.inp.lid_usage, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'aquifers')
            assert isinstance(self.inp.aquifers, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'groundwater')
            assert isinstance(self.inp.groundwater, pd.DataFrame)

        assert hasattr(self.inp, 'junctions')
        assert isinstance(self.inp.junctions, pd.DataFrame)

        assert hasattr(self.inp, 'outfalls')
        assert isinstance(self.inp.outfalls, pd.DataFrame)

        assert hasattr(self.inp, 'storage')
        assert isinstance(self.inp.storage, pd.DataFrame)

        assert hasattr(self.inp, 'dividers')
        assert isinstance(self.inp.dividers, pd.DataFrame)

        assert hasattr(self.inp, 'conduits')
        assert isinstance(self.inp.conduits, pd.DataFrame)

        assert hasattr(self.inp, 'orifices')
        assert isinstance(self.inp.orifices, pd.DataFrame)

        assert hasattr(self.inp, 'weirs')
        assert isinstance(self.inp.weirs, pd.DataFrame)

        assert hasattr(self.inp, 'pumps')
        assert isinstance(self.inp.pumps, pd.DataFrame)

        assert hasattr(self.inp, 'xsections')
        assert isinstance(self.inp.xsections, pd.DataFrame)

        assert hasattr(self.inp, 'curves')
        assert isinstance(self.inp.curves, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'transects')
            assert isinstance(self.inp.transects, pd.DataFrame)

        assert hasattr(self.inp, 'losses')
        assert isinstance(self.inp.losses, pd.DataFrame)

        assert hasattr(self.inp, 'timeseries')
        assert isinstance(self.inp.timeseries, pd.DataFrame)

        assert hasattr(self.inp, 'report')
        assert isinstance(self.inp.report, pd.DataFrame)

        assert hasattr(self.inp, 'tags')
        assert isinstance(self.inp.tags, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, 'map')
            assert isinstance(self.inp.map, pd.DataFrame)

        assert hasattr(self.inp, 'coordinates')
        assert isinstance(self.inp.coordinates, pd.DataFrame)

        assert hasattr(self.inp, 'vertices')
        assert isinstance(self.inp.vertices, pd.DataFrame)

        assert hasattr(self.inp, 'polygons')
        assert isinstance(self.inp.polygons, pd.DataFrame)

        assert hasattr(self.inp, 'symbols')
        assert isinstance(self.inp.symbols, pd.DataFrame)


class Test_SWMMInpFile(base_SWMMInpFileMixin):
    def setup(self):
        self.known_path = data_path(os.path.join('swmm', 'test_inp.inp'))
        self.inp = SWMMInpFile(self.known_path)