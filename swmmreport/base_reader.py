from io import StringIO

import pandas as pd

class BaseReader(object):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path, endline='  \n'):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        self.path = path
        self.endline = endline
        self._orig_file = None

        self._startlines = {}

    @property
    def orig_file(self):
        """
        Unmodified .rpt file read from disk.
        """
        if self._orig_file is None:
            self._orig_file = self.read_file(self.path)
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

    def _find_end(self, linenum, line):
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
        # At the end of every block SWMM adds a space, space, return
        # If this changes in new versions then the `line` var will require
        # an update 
        breaks = []
        for n, l in enumerate(currentfile):
            if l.find(line) > -1:
                breaks.append(n)

        if linenum > breaks[-1]:
            end_row = len(currentfile)
        else:
            end_row = [a for a in breaks if a > linenum][0]

        footers = int(len(currentfile) - end_row)
        return footers

    def read_file(self, filename):
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
        blockstart, comment_lines = self._startlines[block]

        return self._find_line(blockstart) + comment_lines #b/c variable comment lines

    def raw_block(self, block):
        """
        Returns the string representation of the block.
        """
        skiprows = self.find_block(block)
        skipfooter = self._find_end(skiprows, self.endline)

        return ''.join(self.orig_file[skiprows:-skipfooter])

    def _make_df(self, block, names, **kwargs):
        """
        Helper function to parse pd.DataFrame for result properties.
        """
        return pd.read_csv(StringIO(self.raw_block(block)),
                           sep='\s+', header=None,
                           names=names, index_col=[0], **kwargs)
