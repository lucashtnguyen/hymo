from .base_reader import BaseReader

import pandas as pd

class SWMMReportFile(BaseReader):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        BaseReader.__init__(self, path)

        # check units
        self.unit = self.orig_file[self.find_line_num('Flow Units')].split('.')[-1].strip().upper()

        # check swmm version
        self.version = self.orig_file[self.find_line_num('VERSION')].split(' - ')[1].split(' ')[1]

        self._headers = _ReportHeaders(self.unit)

        # INPUTS == YES Blocks
        self._element_count = None
        self._raingage_summary = None
        self._subcatchment_summary = None
        self._node_summary = None
        self._link_summary = None
        self._cross_section_summary = None

        # Continuity Data Blocks
        self._runoff_quantity_continuity = None
        self._flow_routing_continuity = None

        # Results Blocks
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
            'element_count': ('Element Count', 2),
            'raingage_summary': ('Raingage Summary', 5),
            'subcatchment_summary': ('Subcatchment Summary', 5),
            'node_summary': ('Node Summary', 5),
            'link_summary': ('Link Summary', 4),
            'cross_section_summary': ('Cross Section Summary', 5),
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
    def element_count(self):
        """
        The number of elements used in your simulation.
        Created by INPUTS = YES in [REPORT] section of input file
        """
        if self._element_count is None:
            names, dtype = self._headers.element_count

        self._element_count = self._make_df('element_count', sep='\.+', header=None, index_col=[0], dtype=str, engine='python')
        self._element_count.set_index(pd.Index(names), drop=True, inplace=True)  # Replace old row names w/ headers
        self._element_count.rename(columns={self._element_count.columns.values[0]: 'num_elements'}, inplace=True)
        # self._element_count = self._element_count.transpose()

        return self._element_count

    @property
    def raingage_summary(self):
        if self._raingage_summary is None:
            names, dtype = self._headers.raingage_summary

        self._raingage_summary = self._make_df('raingage_summary', sep='\s+', header=None, names=names, index_col=[0], dtype=dtype)

        return self._raingage_summary

    @property
    def subcatchment_summary(self):
        #TODO There is a bug in the SWMM Report File generator that doesn't put a space between the Area and Width
        # if the Area is too large. We need to split it based on two places after the decimal point.
        if self._subcatchment_summary is None:
            names, dtype = self._headers.subcatchment_summary

        self._subcatchment_summary = self._make_df('subcatchment_summary', sep='\s+', header=None, names=names, index_col=[0], dtype=dtype)

        return self._subcatchment_summary

    @property
    def node_summary(self):
        if self._node_summary is None:
            names, dtype = self._headers.node_summary

        self._node_summary = self._make_df('node_summary', sep='\s+', header=None, names=names, index_col=[0], dtype=dtype)

        return self._node_summary

    @property
    def link_summary(self):
        if self._link_summary is None:
            names, dtype = self._headers.link_summary

        self._link_summary = self._make_df('link_summary', sep='\s+', header=None, names=names, index_col=[0], dtype=dtype)

        return self._link_summary

    @property
    def cross_section_summary(self):
        if self._cross_section_summary is None:
            names, dtype = self._headers.cross_section_summary

        self._cross_section_summary = self._make_df('cross_section_summary', sep='\s+', header=None, names=names, index_col=[0], dtype=dtype)
        return self._cross_section_summary

    @property
    def runoff_quantity_continuity(self):
        if self._runoff_quantity_continuity is None:
            names, dtype = self._headers.runoff_quantity_continuity

        var_conversion = {'Total Precipitation': 'Total_Precipitation', 'Evaporation Loss': 'Evaporation_Loss',
                          'Infiltration Loss': 'Infiltration_Loss', 'Surface Runoff': 'Surface_Runoff',
                          'Final Storage': 'Final_Storage', 'Continuity Error (%)': 'Continuity_Error_pcnt'}

        self._runoff_quantity_continuity = pd.DataFrame(columns=names)
        for var in var_conversion:
            line_number = self.find_line_num(var)
            data = self.orig_file[line_number].split()
            if var != 'Continuity Error (%)':
                data = pd.Series([data[3], data[4]], index=[names[0], names[1]], name = var_conversion[var])
            else:
                data = pd.Series([data[4], data[4]], index=[names[0], names[1]], name = var_conversion[var])

            self._runoff_quantity_continuity = self._runoff_quantity_continuity.append(data)

        return self._runoff_quantity_continuity

    @property
    def flow_routing_continuity(self):
        if self._flow_routing_continuity is None:
            names, dtype = self._headers.flow_routing_continuity

        var_conversion = {'Dry Weather Inflow': 'Dry_Weather_Inflow',
                          'Wet Weather Inflow': 'Wet_Weather_Inflow',
                          'Groundwater Inflow': 'Groundwater_Inflow',
                          'RDII Inflow': 'RDII_Inflow',
                          'External Inflow': 'External_Inflow',
                          'External Outflow': 'External_Outflow',
                          'Flooding Loss': 'Flooding_Loss',
                          'Evaporation Loss': 'Evaporation_Loss',
                          'Exfiltration Loss': 'Exfiltration_Loss',
                          'Initial Stored Volume': 'Intial_Stored_Volume',
                          'Final Stored Volume': 'Final_Stored_Volume',
                          'Continuity Error (%)': 'Continuity_Error_pcnt'
                        }

        self._flow_routing_continuity = pd.DataFrame(columns=names)
        for var in var_conversion:
            line_number = self.find_line_num(var)

            # There are two 'Evaporation Loss' sections: This will find the second one
            if var == 'Evaporation Loss':
                subdata = self.orig_file[line_number+1:]
                line_number = self.find_line_num(var, lookup=subdata) + line_number

            data = list(filter(lambda x: '.' in x, self.orig_file[line_number].split()))

            if var != 'Continuity Error (%)':
                data = pd.Series([data[1], data[2]], index=[names[0], names[1]], name=var_conversion[var])

            # Write the continuity error twice since it has no units
            else:
                data = pd.Series([data[1], data[1]], index=[names[0], names[1]], name=var_conversion[var])

            self._flow_routing_continuity = self._flow_routing_continuity.append(data)
        return self._flow_routing_continuity

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
            drop_from_index = [_ for _ in df.index if '-------------------' in _]
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
    def __init__(self, ftype):
        self.ftype = ftype.upper().strip()

        if self.ftype not in ['CFS', 'LPS']:
            e = 'Only "CFS" and "LPS" supported.'
            raise ValueError(e)

    @property
    def element_count(self):
        # names are the same for both CFS and LPS
        names = [
            'Rain_gages', 'Subcatchments',
            'Nodes', 'Links',
            'Pollutants', 'Land_uses'
        ]
        dtype = {'Rain_gages': str}
        return names, dtype


    @property
    def raingage_summary(self):
        names = [ 'Name', 'Data_Source',
                  'Data_Type', 'Recording_Interval_time',
                  'Recording_Interval_units'
                ]
        dtype = {'Name': str}
        return names, dtype

    @property
    def subcatchment_summary(self):
        names = [ 'Name', 'Area',
                  'Width', '%Imperv',
                  '%Slope', 'Rain_Gage',
                  'Outlet'
        ]
        dtype = {'Name': str}
        return names, dtype

    @property
    def node_summary(self):
        names = [ 'Name', 'Type',
                  'Invert Elev.', 'Max. Depth',
                  'Ponded_Area', 'External_Inflow'
        ]
        dtype = {'Name': str}
        return names, dtype

    @property
    def link_summary(self):
        names = [ 'Name', 'From_Node',
                  'To_Node', 'Type',
                  'Length', '%Slope',
                  'Roughness'
        ]

        dtype = {'Name': str}
        return names, dtype

    @property
    def cross_section_summary(self):
        names = ['Conduit', 'Shape',
                 'Full_Depth', 'Full_Area',
                 'Hyd._Rad.', 'Max_Width',
                 'No_of_Barrels', 'Full_Flow'
        ]

        dtype = {'Conduit': str}
        return names, dtype

    @property
    def runoff_quantity_continuity(self):
        if self.ftype == 'CFS':
            names = ['Volume_acre_feet', 'Depth_inches']
        elif self.ftype == 'LPS':
            names = ['Volume_hectare_feet', 'Depth_mm']

        dtype = {'Volume_acre_feet': str}

        return names, dtype

    @property
    def flow_routing_continuity(self):
        if self.ftype == 'CFS':
            names = ['Volume_acre_feet', 'Depth_inches']
        elif self.type == 'LPS':
            names = ['Volume_hectare_feet', 'Depth_mm']

        dtype = {'Volume_acre_feet': str}
        return names, dtype

    @property
    def subcatchment_runoff_results(self):
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
