import pytest
from pkg_resources import resource_filename

import pytest
import pandas as pd
import pandas.util.testing as pdtest

from swmmreport import ReportFile
from .utils import data_path

class base_ReportFileMixin(object):
    def teardown(self):
        None

    def test_attributes(self):
        assert hasattr(self.rpt, 'path')
        assert isinstance(self.rpt.path, str)

        assert hasattr(self.rpt, 'orig_file')
        assert isinstance(self.rpt.orig_file, list)

        assert hasattr(self.rpt, 'subcatchment_runoff_results')
        assert isinstance(self.rpt.subcatchment_runoff_results, pd.DataFrame)

        assert hasattr(self.rpt, 'node_depth_results')
        assert isinstance(self.rpt.node_depth_results, pd.DataFrame)

        assert hasattr(self.rpt, 'node_inflow_results')
        assert isinstance(self.rpt.node_inflow_results, pd.DataFrame)

        assert hasattr(self.rpt, 'node_surcharge_results')
        assert isinstance(self.rpt.node_surcharge_results, pd.DataFrame)
        
        assert hasattr(self.rpt, 'node_flooding_results')
        assert isinstance(self.rpt.node_flooding_results, pd.DataFrame)

        assert hasattr(self.rpt, 'storage_volume_results')
        assert isinstance(self.rpt.storage_volume_results, pd.DataFrame)

        assert hasattr(self.rpt, 'outfall_loading_results')
        assert isinstance(self.rpt.outfall_loading_results, pd.DataFrame)

        assert hasattr(self.rpt, 'link_flow_results')
        assert isinstance(self.rpt.link_flow_results, pd.DataFrame)

        assert hasattr(self.rpt, 'flow_classification_results')
        assert isinstance(self.rpt.flow_classification_results, pd.DataFrame)
       
        assert hasattr(self.rpt, 'conduit_surcharge_results')
        assert isinstance(self.rpt.conduit_surcharge_results, pd.DataFrame)


class Test_ReportFile(base_ReportFileMixin):
    def setup(self):
        # TODO
        # subcatchment results

        self.known_path = data_path('test_rpt.rpt')
        self.node_surcharge_file = data_path('test_node_surcharge_data.csv')
        self.node_depth_file = data_path('test_node_depth_data.csv')
        self.node_inflow_file = data_path('test_node_inflow_data.csv')
        self.node_flooding_file = data_path('test_node_flooding_data.csv')
        self.storage_volume_file = data_path('test_storage_volume_data.csv')
        self.outfall_loading_file = data_path('test_outfall_loading_data.csv')
        self.link_flow_file = data_path('test_link_flow_data.csv')
        self.flow_classification_file = data_path('test_flow_classification_data.csv')
        self.conduit_surcharge_file = data_path('test_conduit_surcharge_data.csv')

        self.rpt = ReportFile(self.known_path)

        self.known_node_surcharge_results = pd.read_csv(
            self.node_surcharge_file, index_col=[0])
        self.known_node_depth_results = pd.read_csv(
            self.node_depth_file, index_col=[0])
        self.known_node_inflow_results = pd.read_csv(
            self.node_inflow_file, index_col=[0])
        self.known_node_flooding_results = pd.read_csv(
            self.node_flooding_file, index_col=[0])
        self.known_storage_volume_results = pd.read_csv(
            self.storage_volume_file, index_col=[0])
        self.known_outfall_loading_results = pd.read_csv(
            self.outfall_loading_file, index_col=[0])
        self.known_link_flow_results = pd.read_csv(
            self.link_flow_file, index_col=[0])
        self.known_flow_classification_results = pd.read_csv(
            self.flow_classification_file, index_col=[0])
        self.known_conduit_surcharge_results = pd.read_csv(
            self.conduit_surcharge_file, index_col=[0])


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

    def test_storage_volume_results(self):
        pdtest.assert_frame_equal(
            self.rpt.storage_volume_results,
            self.known_storage_volume_results
        )
    def test_outfall_loading_results(self):
        pdtest.assert_frame_equal(
            self.rpt.outfall_loading_results,
            self.known_outfall_loading_results
        )
    def test_link_flow_results(self):
        pdtest.assert_frame_equal(
            self.rpt.link_flow_results,
            self.known_link_flow_results
        )
    def test_flow_classification_results(self):
        pdtest.assert_frame_equal(
            self.rpt.flow_classification_results,
            self.known_flow_classification_results
        )
    def test_conduit_surcharge_results(self):
        pdtest.assert_frame_equal(
            self.rpt.conduit_surcharge_results,
            self.known_conduit_surcharge_results
        )