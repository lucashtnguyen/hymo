from .base_reader import BaseReader

import pandas as pd

class InpFile(BaseReader):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        BaseReader.__init__(self, path)

        self._options = None
        self._evaporation = None
        self._temperature = None
        self._raingages = None
        self._subcatchments = None
        self._subareas = None
        self._infiltration = None
        self._lid_controls = None
        self._lid_usage = None
        self._aquifers = None
        self._groundwater = None
        self._junctions = None
        self._outfalls = None
        self._storage = None
        self._conduits = None
        self._orifices = None
        self._weirs = None
        self._xsections = None
        self._curves = None
        self._timeseries = None
        self._report = None
        self._tags = None
        self._map = None
        self._coordinates = None
        self._vertices = None
        self._polygons = None
        self._symbols = None

        self._startlines = {
            # Because the user can add comments into the swmm.inp
            # this will require a slightly different approach.
            # All skiplines will be `2` assuming no comments,
            # direct to data. Then we will remove all comments
            # using the function _clean_comments().

            # dict = {'block_name': ('rpt_header', n_comment_lines)}
            'title': ('[TITLE]', 2),
            'options': ('[OPTIONS]', 2),
            'evaporation': ('[EVAPORATION]', 2),
            'temperature': ('[TEMPERATURE]', 2), # requires special parsing
            'raingages': ('[RAINGAGES]', 2),
            'subcatchments': ('[SUBCATCHMENTS]', 2),
            'subareas': ('[SUBAREAS]', 2),
            'infiltration': ('[INFILTRATION]', 2),
            'lid_controls': ('[LID_CONTROLS]', 2),
            'lid_usage': ('[LID_USAGE]', 2),
            'aquifers': ('[AQUIFERS]', 2),
            'groundwater': ('[GROUNDWATER]', 2),
            'junctions': ('[JUNCTIONS]', 2),
            'outfalls': ('[OUTFALLS]', 2),
            'storage': ('[STORAGE]', 2),
            'conduits': ('[CONDUITS]', 2),
            'orifices': ('[ORIFICES]', 2),
            'outlets': ('[OUTLETS]', 2),
            'weirs': ('[WEIRS]', 2),
            'xsections': ('[XSECTIONS]', 2),
            'curves': ('[CURVES]', 2),
            'timeseries': ('[TIMESERIES]', 2),
            'report': ('[REPORT]', 2),
            'tags': ('[TAGS]', 2),
            'map': ('[MAP]', 2),
            'coordinates': ('[COORDINATES]', 2),
            'vertices': ('[VERTICES]', 2),
            'polygons': ('[POLYGONS]', 2),
            'symbols': ('[SYMBOLS]', 2),
        }

    def BlockDoesNotExistError(self):
        raise(NotImplementedError)
        # TODO
        # need some error handling when a block
        # is not in the inp.

    def _check_headers(self):
        raise(NotImplementedError)
        # check that all of the header blocks are accounted for
        # raise an error if they are not
        # we should consider letter case here as well.
        # consider making a modified file object with title case?

    def _clean_comments(self, df, comment=';'):
        drop_list = [_ for _ in df.index if _[0] == comment]

        return df.drop(drop_list, axis=0)

    @property
    def title(self):
        raise(NotImplementedError)
        # will require special parsing as it is just text
    
    @property
    def options(self):
        if self._options is None:
            names = ['Option', 'Value']

            self._options = self._clean_comments(
                self._make_df('options', names, line='['))

        return self._options

    @property
    def evaporation(self):
        # this might need special parsing.
        # Can't tell from sample

        if self._evaporation is None:
            names = ['Data_Source', 'Parameters']

            self._evaporation = self._clean_comments(
                self._make_df('evaporation', names, line='['))

        return self._evaporation

    @property
    def temperature(self):
        # requires special parsing
        raise(NotImplementedError)
        if self._temperature is None:
            names = ['Data_Element', 'Values']

            self._temperature = self._clean_comments(
                self._make_df('temperature', names, line='['))

        return self._temperature

    @property
    def raingages(self):
        if self._raingages is None:
            names = [
                'Name', 'Format',
                'Interval', 'SCF',
                'Source', 'Path'
            ]

            self._raingages = self._clean_comments(
                self._make_df('raingages', names, line='['))

        return self._raingages


    @property
    def subcatchments(self):
        if self._subcatchments is None:
            names = [
                'Name', 'Rain_Gage',
                'Outlet', 'Area',
                'Pcnt_Imperv', 'Width',
                'Pecnt_Slope', 'CurbLen',
                'SnowPack'
            ]

            self._subcatchments = self._clean_comments(
                self._make_df('subcatchments', names, line='['))

        return self._subcatchments

    @property
    def subareas(self):
        if self._subareas is None:
            names = [
                'Subcatchment', 'N_Imperv',
                'N_Perv', 'S_Imperv',
                'S_Perv', 'PctZero',
                'RouteTo', 'PctRouted'
            ]

            self._subareas = self._clean_comments(
                self._make_df('subareas', names, line='['))

        return self._subareas