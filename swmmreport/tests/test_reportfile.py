import pytest
from pkg_resources import resource_filename

import pytest
import pandas as pd
import pandas.util.testing as pdtest

from swmmreport import ReportFile


def data_path(filename):
    path = resource_filename("swmmreport.tests._data", filename)
    return path

class base_ReportFileMixin(object):
    known_node_surcharge_columns = [
        'Type', 'Hours',
        'Max_Above_Crown_Feet', 'Min_Below_Rim_Feet'
    ]
    known_node_depth_columns = [
        'Type', 'Avg_Depth_Feet', 'Max_Depth_Feet',
        'Max_HGL_Feet', 'Day_of_max', 'Time_of_max', 'Reported_Max'
    ]
    known_node_inflow_columns = [
        'Type', 'Maximum_Lateral_Inflow_cfs', 'Maximum_Total_Inflow_CFS',
        'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
        'Lateral_Inflow_Volume_mgals', 'Total_Inflow_Volume_mgals',
        'Flow_Balance_Error_Percent', 'flag'
    ]
    known_node_flooding_columns = [
        'Hours_Flooded', 'Maximum_Rate_cfs',
        'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
        'Total_Flood_Volume_mgal', 'Maximum_Ponded_Depth_ft'
    ]

    def teardown(self):
        None

    def test_attributes(self):
        assert hasattr(self.rpt, 'path')
        assert isinstance(self.rpt.path, str)

        assert hasattr(self.rpt, 'orig_file')
        assert isinstance(self.rpt.orig_file, list)

        assert hasattr(self.rpt, 'node_surcharge_results')
        assert isinstance(self.rpt.node_surcharge_results, pd.DataFrame)
        for col in self.known_node_surcharge_columns:
            assert col in self.rpt.node_surcharge_results.columns.tolist()

        assert hasattr(self.rpt, 'node_depth_results')
        assert isinstance(self.rpt.node_depth_results, pd.DataFrame)
        for col in self.known_node_depth_columns:
            assert col in self.rpt.node_depth_results.columns.tolist()

        assert hasattr(self.rpt, 'node_inflow_results')
        assert isinstance(self.rpt.node_inflow_results, pd.DataFrame)
        for col in self.known_node_inflow_columns:
            assert col in self.rpt.node_inflow_results.columns.tolist()

        assert hasattr(self.rpt, 'node_flooding_results')
        assert isinstance(self.rpt.node_flooding_results, pd.DataFrame)
        for col in self.known_node_flooding_columns:
            assert col in self.rpt.node_flooding_results.columns.tolist()

        #TODO
        with pytest.raises(NotImplementedError):
            assert hasattr(self.rpt, 'storage_volume_results')
            assert isinstance(self.rpt.storage_volume_results, pd.DataFrame)
            for col in self.known_storage_volume_columns:
                assert col in self.rpt.storage_volume_results.columns.tolist()

        with pytest.raises(NotImplementedError):
            assert hasattr(self.rpt, 'outfall_loading_results')
            assert isinstance(self.rpt.outfall_loading_results, pd.DataFrame)
            for col in self.known_outfall_loading_columns:
                assert col in self.rpt.outfall_loading_results.columns.tolist()

        with pytest.raises(NotImplementedError):
            assert hasattr(self.rpt, 'link_flow_results')
            assert isinstance(self.rpt.link_flow_results, pd.DataFrame)
            for col in self.known_link_flow_columns:
                assert col in self.rpt.link_flow_results.columns.tolist()

        with pytest.raises(NotImplementedError):
            assert hasattr(self.rpt, 'flow_classification_results')
            assert isinstance(self.rpt.flow_classification_results, pd.DataFrame)
            for col in self.known_flow_classification_columns:
                assert col in self.rpt.flow_classification_results.columns.tolist()

        with pytest.raises(NotImplementedError):
            assert hasattr(self.rpt, 'conduit_surcharge_results')
            assert isinstance(self.rpt.conduit_surcharge_results, pd.DataFrame)
            for col in self.known_conduit_surcharge_columns:
                assert col in self.rpt.conduit_surcharge_results.columns.tolist()


class Test_ReportFile(base_ReportFileMixin):
    def setup(self):
        self.known_path = data_path('test_rpt.rpt')
        self.node_surcharge_file = data_path('test_node_surcharge_data.csv')
        self.node_depth_file = data_path('test_node_depth_data.csv')
        self.node_inflow_file = data_path('test_node_inflow_data.csv')
        self.node_flooding_file = data_path('test_node_flooding_data.csv')
        # self.storage_volume_file = data_path('storage_volume_data.csv')
        # self.outfall_loading_file = data_path('outfall_loading_data.csv')
        # self.link_flow_file = data_path('link_flow_data.csv')
        # self.flow_classification_file = data_path('flow_classification_data.csv')
        # self.conduit_surcharge_file = data_path('conduit_surcharge_data.csv')

        self.rpt = ReportFile(self.known_path)

        self.known_node_surcharge_results = pd.read_csv(
            self.node_surcharge_file, index_col=[0])
        self.known_node_depth_results = pd.read_csv(
            self.node_depth_file, index_col=[0])
        self.known_node_inflow_results = pd.read_csv(
            self.node_inflow_file, index_col=[0])
        self.known_node_flooding_results = pd.read_csv(
            self.node_flooding_file, index_col=[0])
        #TODO
        # self.known_storage_volume_results = pd.read_csv(
        #     self.storage_volume_file, index_col=[0])
        # self.known_outfall_loading_results = pd.read_csv(
        #     self.outfall_loading_file, index_col=[0])
        # self.known_link_flow_results = pd.read_csv(
        #     self.link_flow_file, index_col=[0])
        # self.known_flow_classification_results = pd.read_csv(
        #     self.flow_classification_file, index_col=[0])
        # self.known_conduit_surcharge_results = pd.read_csv(
        #     self.conduit_surcharge_file, index_col=[0])


    def test_node_depth_results(self):
        pdtest.assert_frame_equal(
            self.rpt.node_depth_results,
            self.known_node_depth_results
        )

    def test_node_surcharge_results(self):
        pdtest.assert_frame_equal(
            self.rpt.node_surcharge_results,
            self.known_node_surcharge_results
        )

    def test_node_inflow_results(self):
        pdtest.assert_frame_equal(
            self.rpt.node_inflow_results,
            self.known_node_inflow_results
        )
    
    def test_node_flooding_results(self):
        pdtest.assert_frame_equal(
            self.rpt.node_flooding_results,
            self.known_node_flooding_results
        )

    #TODO
    # def test_storage_volume_results(self):
    #     pdtest.assert_frame_equal(
    #         self.rpt.storage_volume_results,
    #         self.known_storage_volume_results
    #     )
    # def test_outfall_loading_results(self):
    #     pdtest.assert_frame_equal(
    #         self.rpt.outfall_loading_results,
    #         self.known_outfall_loading_results
    #     )
    # def test_link_flow_results(self):
    #     pdtest.assert_frame_equal(
    #         self.rpt.link_flow_results,
    #         self.known_link_flow_results
    #     )
    # def test_flow_classification_results(self):
    #     pdtest.assert_frame_equal(
    #         self.rpt.flow_classification_results,
    #         self.known_flow_classification_results
    #     )
    # def test_conduit_surcharge_results(self):
    #     pdtest.assert_frame_equal(
    #         self.rpt.conduit_surcharge_results,
    #         self.known_conduit_surcharge_results
    #     )