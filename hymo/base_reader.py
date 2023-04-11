from pathlib import PurePath
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
        if isinstance(path, PurePath):
            path = path.resolve().as_posix()

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

    def find_line_num(self, line, lookup=None):
        """
        Given a text string returns the line number that the string
        appears in.

        Requires:
        - line: str, text to look up.

        Returns:
        - n: int, the line number where line exists.
        """
        if lookup is None:
            currentfile = self.orig_file.copy()
        else:
            currentfile = lookup.copy()
        for n, l in enumerate(currentfile):
            if l.find(line) > -1:
                break
        return n

    def _find_end(self, linenum, line, lookup=None):
        """
        Given the start of the block returns the number of rows
        needed to for skipfooter in pandas.read_table to only read
        the block.

        Requires:
        - line: str, text to look up.

        Returns:
        - n: int, the line number where line exists.
        """
        if lookup is None:
            currentfile = self.orig_file.copy()
        else:
            currentfile = lookup.copy()
        # At the end of every block SWMM adds a space, space, return
        # If this changes in new versions then the `line` var will require
        # an update
        breaks = []
        for n, l in enumerate(currentfile):
            if l.find(line) > -1:
                breaks.append(n)

        if linenum > breaks[-1]:
            footers = len(currentfile) * -1
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

        if isinstance(filename, str):
            with open(filename, 'r') as openfile:
                lines = openfile.readlines()
        else:
            try: # is StingIO?
                lines = filename.readlines()
            except:
                raise
        return lines

    def find_block(self, block, lookup=None):
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

        return self.find_line_num(blockstart, lookup) + comment_lines #b/c variable comment lines

    def raw_block(self, block):
        """
        Returns the string representation of the block.
        """
        skiprows = self.find_block(block)
        skipfooter = self._find_end(skiprows, self.endline)

        return ''.join(self.orig_file[skiprows:-skipfooter])

    def clean_block(self, block, comment):
        """
        Returns the string representation of the block.
        """
        skiprows = self.find_block(block)
        skipfooter = self._find_end(skiprows, self.endline)

        lines = [_ for _ in self.orig_file[skiprows:-skipfooter] if _[0] != comment]

        return ''.join(lines)

    def _make_df(self, block, comment=None, **kwargs):
        """
        Helper function to parse pd.DataFrame for result properties.
        """
        if comment is not None:
            string_block = self.clean_block(block, comment)
        else:
            string_block = self.raw_block(block)

        engine = kwargs.pop('engine', 'python')

        return pd.read_csv(StringIO(string_block), engine=engine, **kwargs)

    def infer_columns(self, start_line_str, blank_space, n_lines):
        def replace(x):
            """Helper function to convert string to checksum array"""
            if x == ' ':
                return '0,'
            else:
                return '1,'

        def list_replace(y):
            """Helper for replace in lists"""
            return ''.join([replace(_) for _ in y])

        def sanitizer1(s):
            """Helper to remove special chars to conform to PEP"""
            for replace in list('!@#$%^&*()-+={}[]:;<>/?') + list(' '):
                s = s.replace(replace, '_')
            return s

        def sanitizer2(s):
            """Recursive func to remove double '_' from sanitizer()"""
            if '__' in s:
                return santize2(s.replace('__', '_'))
            else:
                return s

        def sanitizer(s):
            """Helper to standardize column names"""
            return sanitizer2(sanitizer1(s))

        # parse the start/end of the actual column names
        start = self.find_line_num(start_line_str) + blank_space + 1
        end = start + n_lines
        column_string_list = self.orig_file[start:end]

        # turn the the string into a checksum array and find occurances
        # where only spaces
        checksum = '\n'.join([list_replace(_) for _ in column_string_list])
        base_array = pd.read_csv(StringIO(checksum), header=None)
        bool_array = base_array.any()
        bool_shifted = base_array.any().shift(1)

        diff = bool_array.sub(bool_shifted)

        # need to start the list at n=0
        column_widths = [0]
        column_widths += diff[diff < 0].index.tolist()

        # might need to go to the end sometimes? if so uncomment:
            # column_widths += [t3.index.max()]

        # do you even list comprehension, bro?
        final_cols = [
            sanitizer(' '.join(c).strip()) for c in
                zip(*[[csl[a1+1:a2+1].strip() for a1, a2 in
                    zip(column_widths, column_widths[1:])] for csl in
                        column_string_list])
        ]

        return final_cols
