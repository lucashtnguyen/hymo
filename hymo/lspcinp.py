from .base_reader import BaseReader


class LSPCInpFile(BaseReader):
    """
    A class to read a LSPC model inp file.
    """

    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing LCPS model .inp.
        """
        BaseReader.__init__(self, path, endline="c-")

        self._c70 = None
        self._c90 = None
        self._c10 = None
        self._c15 = None
        self._c60 = None

        self._startlines = {
            "c10": ("c10", 14),
            "c15": ("c15", 6),
            "c60": ("c60", 8),
            "c70": ("c70", 7),
            "c90": ("c90", 11),
        }

    def _clean_comments(self, df, comment="c"):
        drop_list = [_ for _ in df.index if str(_)[0] == comment]

        return df.drop(drop_list, axis=0)

    @staticmethod
    def _add_suffixes(names, ncols, nrepeat):
        nnames = len(names)
        nrepeats = int((ncols - (nnames - nrepeat)) / nrepeat)
        suffixes = [i + 1 for i in range(nrepeats)]
        _names = names[:-nrepeat] + [
            n + str(i) for i in suffixes for n in names[-nrepeat:]
        ]

        return _names

    @property
    def c10(self):
        if self._c10 is None:
            _names = ["wfileid", "wfilename", "wparamnum", "wparamid"]
            nrepeat = 1

            self._c10 = self._clean_comments(
                self._make_df("c10", sep="\s+", header=None, skiprows=1)
            )

            ncols = len(self._c10.columns)
            names = self._add_suffixes(_names, ncols, nrepeat)

            self._c10.columns = names

        return self._c10

    @property
    def c15(self):
        if self._c15 is None:
            _names = ["wstationid", "wfilenum", "wfileid"]
            nrepeat = 1

            self._c15 = self._clean_comments(
                self._make_df("c15", sep="\s+", header=None, skiprows=1)
            )

            ncols = len(self._c15.columns)
            names = self._add_suffixes(_names, ncols, nrepeat)

            self._c15.columns = names

        return self._c15

    @property
    def c60(self):
        if self._c60 is None:
            _names = ["subbasin", "defid", "nwst", "wst", "wt"]
            nrepeat = 2

            self._c60 = self._clean_comments(
                self._make_df("c60", sep="\s+", header=None, skiprows=1)
            )

            ncols = len(self._c60.columns)
            names = self._add_suffixes(_names, ncols, nrepeat)

            self._c60.columns = names

        return self._c60

    @property
    def c70(self):
        if self._c70 is None:
            names = ["deluid", "deluname", "premult", "petmult"]

            self._c70 = self._clean_comments(
                self._make_df("c70", sep="\s+", header=None, names=names, skiprows=1)
            )

        return self._c70

    @property
    def c90(self):
        if self._c90 is None:
            names = [
                "subbasin",
                "deluid",
                "deluname",
                "perimp",
                "area_ac",
                "slsur",
                "lsur",
            ]

            self._c90 = self._clean_comments(
                self._make_df("c90", sep="\s+", header=None, names=names, skiprows=1)
            )

        return self._c90
