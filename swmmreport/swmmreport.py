import pandas as pd

class ReportFile(object):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        self.path = path
        self._orig_file = None
        self._node_surcharge_results = None
        self._node_depth_results = None
        self._node_inflow_results = None
        self._node_flooding_results = None
        self._storage_volume_results = None
        self._outfall_loading_results = None
        self._link_flow_results = None
        self._flow_classification_results = None
        self._conduit_surcharge_results = None

    @property
    def orig_file(self):
        """
        Unmodified .rpt file read from disk.
        """
        if self._orig_file is None:
            self._orig_file = self.read_rpt(self.path)
        return self._orig_file

    def _find_line(self, line):
        """
        Given a text string returns the line number that the string
        appears in.

        Requires:
        - line: str, text to look up.

        Returns:
        - n: int, the line number where line exists.
        """
        currentfile = self.orig_file.copy()
        for n, l in enumerate(currentfile):
            if l.find(line) > -1:
                break
        return n

    def _find_end(self, linenum):
        """
        Given the start of the block returns the number of rows
        needed to for skipfooter in pandas.read_table to only read
        the block.

        Requires:
        - line: str, tetx to look up.

        Returns:
        - n: int, the line number where line exists.
        """
        currentfile = self.orig_file.copy()
        line = '  \n'
        breaks = []
        for n, l in enumerate(currentfile):
            if l.find(line) > -1:
                breaks.append(n)
        end_row = [a for a in breaks if a > linenum][0]

        footers = int(len(currentfile) - end_row)
        return footers

    def read_rpt(self, filename):
        """
        A wrapper for the standard `open` function implemented using
        `with`.

        Requires:
        - filename: str, the path to the text file.

        Returns:
        - lines: list, a list of lines from `open(filename).readlines()`
        """

        with open(filename, 'r') as openfile:
            lines = openfile.readlines()
        return lines

    def find_block(self, block):
        """
        Finds the start of a SWMM parameter block such as the
        'Node Surcharge Summary' block.

        Requires:
        - block: str, acceptable values include:
            - 'node_surcharge',
            - 'node_depth'

        Returns:
        blockstart: int, the start of the block after the
        comment lines.
        """
        startlines = {
            #dict = {'block_name': ('rpt_header', n_comment_lines)}
            'node_surcharge': ('Node Surcharge Summary', 9),
            'node_depth': ('Node Depth Summary', 8),
            'node_inflow': ('Node Inflow Summary', 9),
            'node_flooding': ('Node Flooding Summary', 10)
            # todo:
            #'volume':,
            #'loading':,
            #'link_flow':,
            #'classification':,
            #'conduit_surcharge':,
        }


        blockstart, comment_lines = startlines[block]

        return self._find_line(blockstart) + comment_lines #b/c variable comment lines

    @property
    def node_surcharge_results(self):
        """
        The parsed node surcharge results as a pandas DataFrame
        """
        if self._node_surcharge_results is None:
            skiprows = self.find_block('node_surcharge')
            skipfooter = self._find_end(skiprows)
            names = ['Node', 'Type', 'Hours', 'Max_Above_Crown_Feet',
                'Min_Below_Rim_Feet']

            df = pd.read_csv(self.path, sep='\s+', header=None,
                names=names, skiprows=skiprows, skipfooter=skipfooter, index_col=[0])
            self._node_surcharge_results = df

        return self._node_surcharge_results

    @property
    def node_depth_results(self):
        """
        The parsed node depth results as a pandas DataFrame
        """
        if self._node_depth_results is None:
            skiprows = self.find_block('node_depth')
            skipfooter = self._find_end(skiprows)
            names = ['Node', 'Type', 'Avg_Depth_Feet', 'Max_Depth_Feet',
                'Max_HGL_Feet', 'Day_of_max', 'Time_of_max', 'Reported_Max']

            df = pd.read_csv(self.path, sep='\s+', header=None,
                names=names, skiprows=skiprows, skipfooter=skipfooter, index_col=[0])
            self._node_depth_results = df

        return self._node_depth_results

    @property
    def node_inflow_results(self):
        """
        The parsed node inflow results as a pandas DataFrame
        """
        if self._node_inflow_results is None:
            skiprows = self.find_block('node_inflow')
            skipfooter = self._find_end(skiprows)
            names = [
                'Node', 'Type',
                'Maximum_Lateral_Inflow_cfs', 'Maximum_Total_Inflow_CFS',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Lateral_Inflow_Volume_mgals', 'Total_Inflow_Volume_mgals',
                'Flow_Balance_Error_Percent', 'flag'
            ]
            df = pd.read_csv(self.path, sep='\s+', header=None,
                names=names, skiprows=skiprows, skipfooter=skipfooter, index_col=[0])
            
            self._node_inflow_results = df

        return self._node_inflow_results

    @property
    def node_flooding_results(self):
        if self._node_flooding_results is None:
            skiprows = self.find_block('node_flooding')
            skipfooter = self._find_end(skiprows)
            names = [
                'Node',
                'Hours_Flooded', 'Maximum_Rate_cfs',
                'Time_of_Max_Occurrence_days', 'Time_of_Max_Occurrence_hours',
                'Total_Flood_Volume_mgal', 'Maximum_Ponded_Depth_ft'
            ]
            
            df = pd.read_csv(self.path, sep='\s+', header=None,
                names=names, skiprows=skiprows, skipfooter=skipfooter, index_col=[0])
            
            self._node_flooding_results = df

        return self._node_flooding_results

    @property
    def storage_volume_results(self):
        if self._storage_volume_results is None:
            raise(NotImplementedError)

        return self._storage_volume_results

    @property
    def outfall_loading_results(self):
        if self._outfall_loading_results is None:
            raise(NotImplementedError)

        return self._outfall_loading_results

    @property
    def link_flow_results(self):
        if self._link_flow_results is None:
            raise(NotImplementedError)

        return self._link_flow_results

    @property
    def flow_classification_results(self):
        if self._flow_classification_results is None:
            raise(NotImplementedError)

        return self._flow_classification_results

    @property
    def conduit_surcharge_results(self):
        if self._conduit_surcharge_results is None:
            raise(NotImplementedError)

        return self._conduit_surcharge_results
