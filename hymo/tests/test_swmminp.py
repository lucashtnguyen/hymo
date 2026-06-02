import os

import pandas as pd
import pandas.testing as pdtest
import pytest

from hymo import SWMMInpFile
from hymo.tests import data_path


class base_SWMMInpFileMixin(object):
    def teardown_method(self):
        None

    def test_attributes(self):
        import pytest

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "title")
            assert isinstance(self.inp.title, pd.DataFrame)

        assert hasattr(self.inp, "options")
        assert isinstance(self.inp.options, pd.DataFrame)

        assert hasattr(self.inp, "evaporation")
        assert isinstance(self.inp.evaporation, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "temperature")
            assert isinstance(self.inp.temperature, pd.DataFrame)

        assert hasattr(self.inp, "raingages")
        assert isinstance(self.inp.raingages, pd.DataFrame)

        assert hasattr(self.inp, "subcatchments")
        assert isinstance(self.inp.subcatchments, pd.DataFrame)

        assert hasattr(self.inp, "subareas")
        assert isinstance(self.inp.subareas, pd.DataFrame)

        assert hasattr(self.inp, "infiltration")
        assert isinstance(self.inp.infiltration, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "lid_controls")
            assert isinstance(self.inp.lid_controls, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "lid_usage")
            assert isinstance(self.inp.lid_usage, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "aquifers")
            assert isinstance(self.inp.aquifers, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "groundwater")
            assert isinstance(self.inp.groundwater, pd.DataFrame)

        assert hasattr(self.inp, "junctions")
        assert isinstance(self.inp.junctions, pd.DataFrame)

        assert hasattr(self.inp, "outfalls")
        assert isinstance(self.inp.outfalls, pd.DataFrame)

        assert hasattr(self.inp, "storage")
        assert isinstance(self.inp.storage, pd.DataFrame)

        assert hasattr(self.inp, "dividers")
        assert isinstance(self.inp.dividers, pd.DataFrame)

        assert hasattr(self.inp, "conduits")
        assert isinstance(self.inp.conduits, pd.DataFrame)

        assert hasattr(self.inp, "orifices")
        assert isinstance(self.inp.orifices, pd.DataFrame)

        assert hasattr(self.inp, "weirs")
        assert isinstance(self.inp.weirs, pd.DataFrame)

        assert hasattr(self.inp, "pumps")
        assert isinstance(self.inp.pumps, pd.DataFrame)

        assert hasattr(self.inp, "xsections")
        assert isinstance(self.inp.xsections, pd.DataFrame)

        assert hasattr(self.inp, "curves")
        assert isinstance(self.inp.curves, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "transects")
            assert isinstance(self.inp.transects, pd.DataFrame)

        assert hasattr(self.inp, "losses")
        assert isinstance(self.inp.losses, pd.DataFrame)

        assert hasattr(self.inp, "timeseries")
        assert isinstance(self.inp.timeseries, pd.DataFrame)

        assert hasattr(self.inp, "report")
        assert isinstance(self.inp.report, pd.DataFrame)

        assert hasattr(self.inp, "tags")
        assert isinstance(self.inp.tags, pd.DataFrame)

        with pytest.raises(NotImplementedError):
            assert hasattr(self.inp, "map")
            assert isinstance(self.inp.map, pd.DataFrame)

        assert hasattr(self.inp, "coordinates")
        assert isinstance(self.inp.coordinates, pd.DataFrame)

        assert hasattr(self.inp, "vertices")
        assert isinstance(self.inp.vertices, pd.DataFrame)

        assert hasattr(self.inp, "polygons")
        assert isinstance(self.inp.polygons, pd.DataFrame)

        assert hasattr(self.inp, "symbols")
        assert isinstance(self.inp.symbols, pd.DataFrame)

        assert hasattr(self.inp, "pollutants")
        assert isinstance(self.inp.pollutants, pd.DataFrame)

        assert hasattr(self.inp, "inflows")
        assert isinstance(self.inp.inflows, pd.DataFrame)

        assert hasattr(self.inp, "rdii")
        assert isinstance(self.inp.rdii, pd.DataFrame)

        assert hasattr(self.inp, "hydrographs")
        assert isinstance(self.inp.hydrographs, pd.DataFrame)

        assert hasattr(self.inp, "dwf")
        assert isinstance(self.inp.dwf, pd.DataFrame)


class Test_SWMMInpFile(base_SWMMInpFileMixin):
    def setup_method(self):
        self.known_path = data_path(os.path.join("swmm", "test_inp.inp"))
        self.inp = SWMMInpFile(self.known_path)

    def test_representative_sections_parse_expected_fixture_values(self):
        assert self.inp.options.loc["FLOW_UNITS", "Value"] == "CFS"
        assert self.inp.options.loc["FLOW_ROUTING", "Value"] == "DYNWAVE"

        assert self.inp.raingages.shape == (5, 7)
        assert self.inp.raingages.loc["SCS_6h_2.785in", "Source"] == "TIMESERIES"
        assert self.inp.raingages.loc["SCS_6h_2.785in", "ID"] == "SCS_6h_2.785in"

        assert self.inp.subcatchments.shape == (47, 8)
        assert self.inp.subcatchments.loc["CarE4000", "Outlet"] == "585"
        assert self.inp.subcatchments.loc["CarE4000", "Area"] == 15.374814

        assert self.inp.junctions.shape == (138, 5)
        assert self.inp.junctions.loc["1082", "Invert_Elev"] == 630.37
        assert self.inp.junctions.loc["1082", "Max_Depth"] == 2.63

        assert self.inp.conduits.shape == (135, 8)
        assert self.inp.conduits.loc["C1", "Inlet_Node"] == "J2"
        assert self.inp.conduits.loc["C1", "Length"] == 94.33

    def test_conduit_slopes_for_requested_conduits(self):
        slopes = self.inp.conduit_slopes(["C1", "C10"])

        assert slopes.index.tolist() == ["C1", "C10"]
        assert slopes.loc["C1", "Inlet_Node_Invert_Elev"] == 627.943
        assert slopes.loc["C1", "Outlet_Node_Invert_Elev"] == 625.555
        assert slopes.loc["C1", "Inlet_Pipe_Invert_Elev"] == 627.943
        assert slopes.loc["C1", "Outlet_Pipe_Invert_Elev"] == 625.555
        assert slopes.loc["C1", "Slope"] == pytest.approx(
            (627.943 - 625.555) / 94.33
        )

    def test_conduit_slopes_uses_offsets_as_elevations_when_configured(self):
        self.inp._options = self.inp.options.copy()
        self.inp._options.loc["LINK_OFFSETS", "Value"] = "ELEVATION"
        self.inp._conduits = self.inp.conduits.copy()
        self.inp._conduits.loc["C1", "Inlet_Offset"] = 628.0
        self.inp._conduits.loc["C1", "Outlet_Offset"] = 625.0

        slopes = self.inp.conduit_slopes(["C1"])

        assert slopes.loc["C1", "Inlet_Pipe_Invert_Elev"] == 628.0
        assert slopes.loc["C1", "Outlet_Pipe_Invert_Elev"] == 625.0
        assert slopes.loc["C1", "Slope"] == pytest.approx((628.0 - 625.0) / 94.33)

    def test_conduit_slopes_defaults_to_all_conduits(self):
        slopes = self.inp.conduit_slopes()

        assert len(slopes) == len(self.inp.conduits)
        assert slopes.index.equals(self.inp.conduits.index)
        assert "Slope" in slopes.columns

    @pytest.mark.skip(reason="SWMM .inp column schemas vary by SWMM version.")
    def test_versioned_inp_schema_contract(self):
        assert False

if __name__ == "__main__":
    known_path = data_path(os.path.join("swmm", "test_inp.inp"))
    inp = SWMMInpFile(known_path)
    print(inp.conduits.head())
    print(inp.junctions.head())
    print(inp.xsections.head())
