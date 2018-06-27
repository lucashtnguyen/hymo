from io import StringIO

import pandas as pd

from .base_reader import BaseReader

class SWMMInterfaceFile(BaseReader):

    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        BaseReader.__init__(self, path)

        self._interface = None
        self._header = None
        self._units = None
        self._nodes = None

    @property
    def nodes(self):
        if self._nodes is None:
            n_nodes_txt = "number of nodes"
            node_line_num = self.find_line_num(n_nodes_txt)
            n_nodes = self.orig_file[node_line_num].split("-")[0].strip()

            _nodes = (
                self.orig_file[node_line_num +
                               1: node_line_num + int(n_nodes) + 1]
            )

            self._nodes = [_.strip() for _ in _nodes]

        return self._nodes

    @property
    def units(self):
        if self._units is None:
            n_const_txt = "number of constituents"
            n_const = self.orig_file[
                self.find_line_num(n_const_txt)
            ].split("-")[0].strip()

            const_line_num = self.find_line_num(n_const_txt)
            constituent_info = (
                self.orig_file[const_line_num +
                               1: const_line_num + int(n_const) + 1]
            )

            self._units = {
                line.strip().split(" ")[0]: line.strip().split(" ")[1]
                for line in constituent_info
            }

        return self._units

    @property
    def header(self):
        if self._header is None:
            n_nodes_txt = "number of nodes"
            self._header = "".join(
                self.orig_file[:self.find_line_num(
                    n_nodes_txt) + len(self.nodes) + 1]
            )

        return self._header

    @property
    def interface(self):

        if self._interface is None:

            names = self.infer_columns('Node', -1, 1)
            names[0] = 'Node'

            skiprows = len(self.header.splitlines())+1
            
            block =  ''.join(self.orig_file[skiprows:])

            self._interface = (
                pd.read_csv(
                    StringIO(block), 
                    sep='\s+', header=None,
                    names=names, 
                    index_col=None,
                )
            )


        return self._interface
