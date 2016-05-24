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
        self._orig_file = None #self.read_rpt(path)
        self._surcharge_results = None
        self._depth_results = None

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
        - block: str, acceptable values include: 'surcharge',
            'depth'

        Returns:
        blockstart: int, the start of the block after the
        comment lines.
        """
        startlines = {
            'surcharge': ('Node Surcharge Summary', 9),
            'depth': ('Node Depth Summary', 8),
            # todo:
            #'inflow':,
            #'flooding':,
            #'volume':,
            #'loading':,
            #'link_flow':,
            #'classification':,
            #'conduit_surcharge':,
        }


        blockstart, comment_lines = startlines[block]

        return self._find_line(blockstart) + comment_lines #b/c variable comment lines

    @property
    def surcharge_results(self):
        """
        The parsed surcharge results as a pandas DataFrame
        """
        if self._surcharge_results is None:
            skiprows = self.find_block('surcharge')
            skipfooter = self._find_end(skiprows)
            names = ['Node', 'Type', 'Hours', 'Max_Above_Crown_Feet',
                'Min_Below_Rim_Feet']

            df = pd.read_csv(self.path, sep='\s+', header=None,
                names=names, skiprows=skiprows, skipfooter=skipfooter, index_col=[0])
            self._surcharge_results = df

        return self._surcharge_results

    @property
    def depth_results(self):
        """
        The parsed depth results as a pandas DataFrame
        """
        if self._depth_results is None:
            skiprows = self.find_block('depth')
            skipfooter = self._find_end(skiprows)
            names = ['Node', 'Type', 'Avg_Depth_Feet', 'Max_Depth_Feet',
                'Max_HGL_Feet', 'Day_of_max', 'Time_of_max', 'Reported_Max']

            df = pd.read_csv(self.path, sep='\s+', header=None,
                names=names, skiprows=skiprows, skipfooter=skipfooter, index_col=[0])
            self._depth_results = df

        return self._depth_results

