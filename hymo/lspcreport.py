import pandas as pd

from .base_reader import BaseReader

class LSPCResults(object):
    """
    A light weight LSPC results parser.
    """
    def __init__(self, results_path, summary_path, summary_EOF=-2):
        """
        ---------
        Requires:
        - results_path: str, path to the results.csv results file.
        - summary_path: str, path to the results.out summary file.

        ---------
        Optional:
        - summary_EOF: (-)int, default=-2. Number of end of file comment lines.

        ----------
        Properties:
        - results_path: The path of results_path as input in __init__.
            - Returns: str
        - summary_path: The path of summary_path as input in __init__.
            - Returns: str
        - raw_results: The unmodified csv file of self.results_path as read
            by pandas.read_csv().
            - Returns: pandas.DataFrame
        - raw_summary: A string representation of the raw summary file.
            - Returns: str
        - parsed_summary: A parsed version of self.raw_summary containing the
            units and description of each variable.
            - Returns: pandas.DataFrame
        - parsed_results: The `raw_results` joined to `parsed_summary`
            - Returns: pandas.DataFrame

        """
        if (summary_EOF > 0) or not isinstance(summary_EOF, int):
            e = '`summary_EOF` must be a negative int.'
            raise(ValueError(e))

        self.results_path = results_path
        self.summary_path = summary_path
        self._summary_EOF = summary_EOF

        self._raw_results = None
        self._raw_summary = None
        self._parsed_summary = None

        self._parsed_results = None

    @property
    def raw_results(self):
        """
        The unmodified csv file of self.results_path as read
            by pandas.read_csv().
        Returns: pandas.DataFrame
        """
        if self._raw_results is None:
            self._raw_results = pd.read_csv(self.results_path)
        
        return self._raw_results

    @property
    def raw_summary(self):
        """
        A string representation of the raw summary file.
        Returns: str
        """
        if self._raw_summary is None:
            self.parsed_summary
        return self._raw_summary

    @property
    def parsed_summary(self):
        """
        A parsed version of self.raw_summary containing the
            units and description of each variable.
        Returns: pandas.DataFrame
        """
        if self._parsed_summary is None:
            with open(self.summary_path, 'r') as openfile:
                lines = openfile.readlines()

            # concat the raw lines and stash
            self._raw_summary = ''.join(lines)

            # find the end of the headers
            start_at = [n for n, _ in enumerate(lines) if 'TT Label' in _][0] + 1

            parsed_summary = {}
            for l in lines[start_at:self._summary_EOF]:
                # comment string is "TT " skip 3
                space_split = l[3:].split(' ')
                # variable is the first in the tuple
                var = space_split[0]
                # recreate the description
                desc = ' '.join([_ for _ in space_split[1:] if _ != '']).strip()
                # parse the unit
                unit = l.split(' (')[-1].strip()[:-1]

                parsed_summary[var] = {
                    'unit': unit,
                    'description': desc
                }

            self._parsed_summary = pd.DataFrame(parsed_summary).T

        return self._parsed_summary

    @property
    def parsed_results(self):
        """
        The `raw_results` joined to `parsed_summary`
        Returns: pandas.DataFrame
        """
        if self._parsed_results is None:
            self._parsed_results = self.raw_results.join(self.parsed_summary, on='parmname')
        return self._parsed_results



class LSPCInp(BaseReader):
    """
    A class to read a LSPC model inp file.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing LCPS model .inp.
        """
        BaseReader.__init__(self, path, endline='c-')
        
        self._c70 = None
        self._c90 = None
        
        self._startlines = {
            'c70': ('c70', 7),
            'c90': ('c90', 10),
        }
        
    def _clean_comments(self, df, comment='c'):
        drop_list = [_ for _ in df.index if str(_)[0] == comment]

        return df.drop(drop_list, axis=0)
    
    @property
    def c70(self):
        if self._c70 is None:
            names = ['deluid', 'deluname', 'premult', 'petmult']

            self._c70 = self._clean_comments(
                self._make_df('c70', names, skiprows=1))

        return self._c70
    
    @property
    def c90(self):
        if self._c90 is None:
            names = ['subbasin', 'deluid', 'deluname',
                     'perimp', 'area_ac', 'slsur', 'lsur',]

            self._c90 = self._clean_comments(
                self._make_df('c90', names))

        return self._c90