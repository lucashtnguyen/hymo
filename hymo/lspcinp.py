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
        BaseReader.__init__(self, path, endline='c-')
        
        self._c70 = None
        self._c90 = None
        
        self._startlines = {
            'c70': ('c70', 7),
            'c90': ('c90', 11),
        }
        
    def _clean_comments(self, df, comment='c'):
        drop_list = [_ for _ in df.index if str(_)[0] == comment]

        return df.drop(drop_list, axis=0)
    
    @property
    def c70(self):
        if self._c70 is None:
            names = ['deluid', 'deluname', 'premult', 'petmult']

            self._c70 = self._clean_comments(
                self._make_df('c70', sep='\s+', header=None,
                              names=names, skiprows=1))

        return self._c70
    
    @property
    def c90(self):
        if self._c90 is None:
            names = ['subbasin', 'deluid', 'deluname',
                     'perimp', 'area_ac', 'slsur', 'lsur',]

            self._c90 = self._clean_comments(
                self._make_df('c90', sep='\s+', header=None,
                              names=names, skiprows=1))

        return self._c90