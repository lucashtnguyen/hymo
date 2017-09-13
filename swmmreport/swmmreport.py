from .base_reader import BaseReader

import pandas as pd

class ReportFile(BaseReader):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        BaseReader.__init__(self, path)

        self._node_depth_results = None
        self._node_inflow_results = None
        self._node_surcharge_results = None
        self._node_flooding_results = None
        self._storage_volume_results = None
        self._outfall_loading_results = None
        self._link_flow_results = None
        self._flow_classification_results = None
        self._conduit_surcharge_results = None

        self._startlines = {
            #dict = {'block_name': ('rpt_header', n_comment_lines)}
            'node_depth': ('Node Depth Summary', 8),
            'node_inflow': ('Node Inflow Summary', 9),
            'node_surcharge': ('Node Surcharge Summary', 9),
            'node_flooding': ('Node Flooding Summary', 10),
            'storage_volume': ('Storage Volume Summary', 8),
            'outfall_loading': ('Outfall Loading Summary', 8), #special conditions at end of block
            'link_flow': ('Link Flow Summary', 8),
            'flow_classification': ('Flow Classification Summary', 8),
            'conduit_surcharge': ('Conduit Surcharge Summary', 8) #special conditions EOF
        }
    
    @property
    def node_depth_results(self):
        """
        The parsed node depth results as a pandas DataFrame
        """
        if self._node_depth_results is None:
            #TODO check names and make consistent with new properties
            names = [
                'Node', 'Type',
                'Average_Depth_Feet', 'Maximum_Depth_Feet',
                'Maximum_HGL_Feet', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Reported_Max_Depth_Feet'
            ]

            self._node_depth_results = self._make_df('node_depth', names)

        return self._node_depth_results

    @property
    def node_inflow_results(self):
        """
        The parsed node inflow results as a pandas DataFrame
        """
        if self._node_inflow_results is None:
            names = [
                'Node', 'Type',
                'Maximum_Lateral_Inflow_CFS', 'Maximum_Total_Inflow_CFS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Lateral_Inflow_Volume_mgals', 'Total_Inflow_Volume_mgals',
                'Flow_Balance_Error_Percent', 'flag'
            ]
            
            self._node_inflow_results = self._make_df('node_inflow', names)

        return self._node_inflow_results

    @property
    def node_surcharge_results(self):
        """
        The parsed node surcharge results as a pandas DataFrame
        """
        if self._node_surcharge_results is None:
            #TODO check names and make consistent with new properties
            names = [
                'Node', 'Type',
                'Hours_Surcharged', 'Max_Height_Above_Crown_Feet',
                'Min_Depth_Below_Rim_Feet'
            ]

            self._node_surcharge_results = self._make_df('node_surcharge', names)

        return self._node_surcharge_results

    @property
    def node_flooding_results(self):
        if self._node_flooding_results is None:
            names = [
                'Node',
                'Hours_Flooded', 'Maximum_Rate_CFS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Total_Flood_Volume_mgal', 'Maximum_Ponded_Depth_Feet'
            ]
            
            self._node_flooding_results = self._make_df('node_flooding', names)

        return self._node_flooding_results

    @property
    def storage_volume_results(self):
        if self._storage_volume_results is None:
            names = [
                'Storage_Unit', 'Average_Volume_1000_ft3',
                'Avg_Pcnt_Full', 'Evap_Pcnt_Loss',
                'Exfil_Pcnt_Loss', 'Maximum_Volume_1000_ft3',
                'Max_Pcnt_Full', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Maximum_Outflow_CFS'    
            ]

            self._storage_volume_results = self._make_df('storage_volume', names)

        return self._storage_volume_results

    @property
    def outfall_loading_results(self):
        if self._outfall_loading_results is None:
            # special conditions at end of block
            # summary stats -> parse all and drop sep '---' 
            names = [
                'Outfall_Node', 'Flow_Freq_Pcnt',
                'Avg_Flow_CFS', 'Max_Flow_CFS',
                'Total_Volume_mgal'
            ]
            df = self._make_df('outfall_loading', names)
            # drop sep
            drop_from_index = [_ for _ in df.index if '-' in _]
            df = df.drop(drop_from_index)

            self._outfall_loading_results = df

        return self._outfall_loading_results

    @property
    def link_flow_results(self):
        if self._link_flow_results is None:
            names = [
                'Link', 'Type',
                'Maximum_Flow_CFS', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Maximum_Veloc_ftsec',
                'Max_Full_Flow', 'Max_Full_Depth'
            ]
            self._link_flow_results = self._make_df('link_flow', names)

        return self._link_flow_results

    @property
    def flow_classification_results(self):
        if self._flow_classification_results is None:
            names = [
                'Conduit', 'Adjusted_Actual_Length',
                'Fraction_of_Time_Dry', 'Fraction_of_Time_Up_Dry',
                'Fraction_of_Time_Down_Dry', 'Fraction_of_Time_Sub_Crit',
                'Fraction_of_Time_Sup_Crit', 'Fraction_of_Time_Up_Crit',
                'Fraction_of_Time_Down_Crit', 'Fraction_of_Time_Norm_Ltd',
                'Fraction_of_Time_Inlet_Ctrl',
            ]
            self._flow_classification_results = self._make_df('flow_classification', names)

        return self._flow_classification_results

    @property
    def conduit_surcharge_results(self):
        if self._conduit_surcharge_results is None:
            # There are some EOF lines that we need to exclude.
            # For now the _find_end function detects the end of 
            # block because of the 2xSpace+return.
            names = [
                'Conduit', 'Hours_Full_Both_Ends',
                'Hours_Full_Upstream', 'Hours_Full_Dnstream',
                'Hours_Above_Full_Normal_Flow', 'Hours_Capacity_Limited',
            ]
            self._conduit_surcharge_results = self._make_df('conduit_surcharge', names)

        return self._conduit_surcharge_results
