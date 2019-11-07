from .base_reader import BaseReader

import pandas as pd

class SWMMReportFile(BaseReader):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path, version='5.1.013'):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        - version: str, the full SWMM version. Default is most recent (5.1.013).
        """
        BaseReader.__init__(self, path)

        # check units
        self.unit = self.orig_file[self.find_line_num('Flow Units')].split('.')[-1].strip().upper()
        self.version = version

        self._headers = _ReportHeaders(self.unit)

        self._subcatchment_runoff_results = None
        self._node_depth_results = None
        self._node_inflow_results = None
        self._node_surcharge_results = None
        self._node_flooding_results = None
        self._storage_volume_results = None
        self._outfall_loading_results = None
        self._link_flow_results = None
        self._flow_classification_results = None
        self._conduit_surcharge_results = None
        self._link_pollutant_load_results = None

        self._startlines = {
            #dict = {'block_name': ('rpt_header', n_comment_lines)}
            'subcatchment_runoff': ('Subcatchment Runoff Summary', 8),
            'node_depth': ('Node Depth Summary', 8),
            'node_inflow': ('Node Inflow Summary', 9),
            'node_surcharge': ('Node Surcharge Summary', 9),
            'node_flooding': ('Node Flooding Summary', 10),
            'storage_volume': ('Storage Volume Summary', 8),
            'outfall_loading': ('Outfall Loading Summary', 8), #special conditions at end of block
            'link_flow': ('Link Flow Summary', 8),
            'flow_classification': ('Flow Classification Summary', 8),
            'conduit_surcharge': ('Conduit Surcharge Summary', 8), #special conditions EOF
            'link_pollutant_load': ('Link Pollutant Load Summary', 7)
        }

    @property
    def subcatchment_runoff_results(self):
        """
        The parsed node depth results as a pandas DataFrame
        """
        if self._subcatchment_runoff_results is None:
            names, dtype = self._headers.subcatchment_runoff_results

            self._subcatchment_runoff_results = self._make_df(
                'subcatchment_runoff', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._subcatchment_runoff_results

    @property
    def node_depth_results(self):
        """
        The parsed node depth results as a pandas DataFrame
        """
        if self._node_depth_results is None:
            #TODO check names and make consistent with new properties
            names, dtype = self._headers.node_depth_results

            self._node_depth_results = self._make_df(
                'node_depth', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._node_depth_results

    @property
    def node_inflow_results(self):
        """
        The parsed node inflow results as a pandas DataFrame
        """
        if self._node_inflow_results is None:
            names, dtype = self._headers.node_inflow_results

            self._node_inflow_results = self._make_df(
                'node_inflow', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._node_inflow_results

    @property
    def node_surcharge_results(self):
        """
        The parsed node surcharge results as a pandas DataFrame
        """
        if self._node_surcharge_results is None:
            #TODO check names and make consistent with new properties
            names, dtype = self._headers.node_surcharge_results

            self._node_surcharge_results = self._make_df(
                'node_surcharge', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._node_surcharge_results

    @property
    def node_flooding_results(self):
        if self._node_flooding_results is None:
            names, dtype = self._headers.node_flooding_results

            self._node_flooding_results = self._make_df(
                'node_flooding', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._node_flooding_results

    @property
    def storage_volume_results(self):
        if self._storage_volume_results is None:
            names, dtype = self._headers.storage_volume_results

            self._storage_volume_results = self._make_df(
                'storage_volume', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._storage_volume_results

    @property
    def outfall_loading_results(self):
        if self._outfall_loading_results is None:
            # special conditions at end of block
            # summary stats -> parse all and drop sep '---'

            start_line_str = 'Outfall Loading Summary'
            blank_space = 3
            n_lines = 3

            names = self.infer_columns(start_line_str, blank_space, n_lines)

            # "Outfall Node" needs to be joined
            n = '_'.join(names[:2])
            _ = names.pop(0)
            names[0] = n
            dtype = {'Outfall_Node': str}

            df = self._make_df('outfall_loading', sep='\s+',
                header=None, names=names, index_col=[0], dtype=dtype)

            # drop sep
            drop_from_index = [_ for _ in df.index if '-' in _]
            df = df.drop(drop_from_index)

            self._outfall_loading_results = df

        return self._outfall_loading_results

    @property
    def link_flow_results(self):
        if self._link_flow_results is None:
            names, dtype = self._headers.link_flow_results

            self._link_flow_results = self._make_df(
                'link_flow', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._link_flow_results

    @property
    def flow_classification_results(self):
        if self._flow_classification_results is None:
            names, dtype = self._headers.flow_classification_results

            self._flow_classification_results = self._make_df(
                'flow_classification', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._flow_classification_results

    @property
    def conduit_surcharge_results(self):
        if self._conduit_surcharge_results is None:
            # There are some EOF lines that we need to exclude.
            # For now the _find_end function detects the end of
            # block because of the 2xSpace+return.
            names, dtype = self._headers.conduit_surcharge_results

            self._conduit_surcharge_results = self._make_df(
                'conduit_surcharge', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._conduit_surcharge_results

    @property
    def link_pollutant_load_results(self):
        if self._link_pollutant_load_results is None:
            # there will be more than one pollutant
            # we will need to think about a proper
            # name parser.
            start_line_str = 'Link Pollutant Load Summary'
            blank_space = 3
            n_lines = 2
            dtype = {'Link': str}

            names = self.infer_columns(start_line_str, blank_space, n_lines)

            self._link_pollutant_load_results = self._make_df(
                'link_pollutant_load', sep='\s+', header=None, names=names, 
                index_col=[0], dtype=dtype)

        return self._link_pollutant_load_results


class _ReportHeaders(object):
    """
    _ReportHeaders: What is my purpose?
    Dev: You make headers
    _ReportHeaders: Oh my god
    """
    def __init__(self, ftype, version = '5.1.013'):
        self.ftype = ftype.upper().strip()
        self.version = version

        if self.ftype not in ['CFS', 'LPS']:
            e = 'Only "CFS" and "LPS" supported.'
            raise ValueError(e)


    @property
    def subcatchment_runoff_results(self):
        if self.version != '5.1.013':
            if self.ftype == 'CFS': 
                names = [ 
                    'Subcatchment', 'Total_Precip_in', 
                    'Total_Runon_in', 'Total_Evap_in', 
                    'Total_Infil_in', 'Total_Runoff_in', 
                    'Total_Runoff_mgal', 'Peak_Runoff_CFS', 
                    'Runoff_Coeff'] 

            elif self.ftype == 'LPS': 
                names = [ 
                    'Subcatchment', 'Total_Precip_mm', 
                    'Total_Runon_mm', 'Total_Evap_mm', 
                    'Total_Infil_mm', 'Total_Runoff_mm', 
                    'Total_Runoff_mltr', 'Peak_Runoff_LPS', 
                    'Runoff_Coeff'] 
            dtype = {'Subcatchment': str} 

        elif self.version == '5.1.013':
            if self.ftype == 'CFS':
                names = [
                    'Subcatchment', 'Total_Precip_in',
                    'Total_Runon_in', 'Total_Evap_in',
                    'Total_Infil_in', 'Imperv_Runoff_in', 
                    'Perv_Runoff_in', 'Total_Runoff_in',
                    'Total_Runoff_mgal', 'Peak_Runoff_CFS',
                    'Runoff_Coeff']

            elif self.ftype == 'LPS':
                names = [
                    'Subcatchment', 'Total_Precip_mm',
                    'Total_Runon_mm', 'Total_Evap_mm',
                    'Total_Infil_mm', 'Imperv_Runoff_mm', 
                    'Perv_Runoff_mm', 'Total_Runoff_mm',
                    'Total_Runoff_mltr', 'Peak_Runoff_LPS',
                    'Runoff_Coeff']
            dtype = {'Subcatchment': str}
        return names, dtype

    @property
    def node_depth_results(self):
        if self.ftype == 'CFS':
            names = [
                'Node', 'Type',
                'Average_Depth_Feet', 'Maximum_Depth_Feet',
                'Maximum_HGL_Feet', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Reported_Max_Depth_Feet'
            ]

        elif self.ftype == 'LPS':
            names = [
                'Node', 'Type',
                'Average_Depth_Meters', 'Maximum_Depth_Meters',
                'Maximum_HGL_Meters', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Reported_Max_Depth_Meters'
            ]
        dtype = {'Node': str}
        return names, dtype

    @property
    def node_inflow_results(self):
        if self.ftype == 'CFS':
            names = [
                'Node', 'Type',
                'Maximum_Lateral_Inflow_CFS', 'Maximum_Total_Inflow_CFS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Lateral_Inflow_Volume_mgals', 'Total_Inflow_Volume_mgals',
                'Flow_Balance_Error_Percent', 'flag'
            ]

        elif self.ftype == 'LPS':
            names = [
                'Node', 'Type',
                'Maximum_Lateral_Inflow_LPS', 'Maximum_Total_Inflow_LPS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Lateral_Inflow_Volume_mltr', 'Total_Inflow_Volume_mltr',
                'Flow_Balance_Error_Percent', 'flag'
            ]
        dtype = {'Node': str}
        return names, dtype

    @property
    def node_surcharge_results(self):
        if self.ftype == 'CFS':
            names = [
                'Node', 'Type',
                'Hours_Surcharged', 'Max_Height_Above_Crown_Feet',
                'Min_Depth_Below_Rim_Feet'
            ]

        elif self.ftype == 'LPS':
            names = [
                'Node', 'Type',
                'Hours_Surcharged', 'Max_Height_Above_Crown_Meters',
                'Min_Depth_Below_Rim_Meters'
            ]

        dtype = {'Node': str}
        return names, dtype

    @property
    def node_flooding_results(self):
        if self.ftype == 'CFS':
            names = [
                'Node',
                'Hours_Flooded', 'Maximum_Rate_CFS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Total_Flood_Volume_mgal', 'Maximum_Ponded_Depth_Feet'
            ]

        elif self.ftype == 'LPS':
            names = [
                'Node',
                'Hours_Flooded', 'Maximum_Rate_LPS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Total_Flood_Volume_mltr', 'Maximum_Ponded_Depth_Meters'
            ]

        dtype = {'Node': str}
        return names, dtype

    @property
    def storage_volume_results(self):
        if self.ftype == 'CFS':
            names = [
                'Storage_Unit', 'Average_Volume_1000_ft3',
                'Avg_Pcnt_Full', 'Evap_Pcnt_Loss',
                'Exfil_Pcnt_Loss', 'Maximum_Volume_1000_ft3',
                'Max_Pcnt_Full', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Maximum_Outflow_CFS'
            ]
        elif self.ftype == 'LPS':
            names = [
                'Storage_Unit', 'Average_Volume_1000_m3',
                'Avg_Pcnt_Full', 'Evap_Pcnt_Loss',
                'Exfil_Pcnt_Loss', 'Maximum_Volume_1000_m3',
                'Max_Pcnt_Full', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Maximum_Outflow_LPS'
            ]

        dtype = {'Storage_Unit': str}
        return names, dtype


    @property
    def link_flow_results(self):
        if self.ftype == 'CFS':
            names = [
                'Link', 'Type',
                'Maximum_Flow_CFS', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Maximum_Veloc_ftsec',
                'Max_Full_Flow', 'Max_Full_Depth'
            ]
        elif self.ftype == 'LPS':
            names = [
                'Link', 'Type',
                'Maximum_Flow_LPS', 'Time_of_Max_Occurrence_days',
                'Time_of_Max_Occurrence_hours', 'Maximum_Veloc_msec',
                'Max_Full_Flow', 'Max_Full_Depth'
            ]

        dtype = {'Link': str}
        return names, dtype

    @property
    def flow_classification_results(self):
        names = [
            'Conduit', 'Adjusted_Actual_Length',
            'Fraction_of_Time_Dry', 'Fraction_of_Time_Up_Dry',
            'Fraction_of_Time_Down_Dry', 'Fraction_of_Time_Sub_Crit',
            'Fraction_of_Time_Sup_Crit', 'Fraction_of_Time_Up_Crit',
            'Fraction_of_Time_Down_Crit', 'Fraction_of_Time_Norm_Ltd',
            'Fraction_of_Time_Inlet_Ctrl',
        ]

        dtype = {'Conduit': str}
        return names, dtype

    @property
    def conduit_surcharge_results(self):
        names = [
            'Conduit', 'Hours_Full_Both_Ends',
            'Hours_Full_Upstream', 'Hours_Full_Dnstream',
            'Hours_Above_Full_Normal_Flow', 'Hours_Capacity_Limited',
        ]

        dtype = {'Conduit': str}
        return names, dtype