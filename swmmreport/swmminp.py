import warnings
import pandas as pd

from .base_reader import BaseReader

class InpFile(BaseReader):
    """
    A class to read a SWMM model report file.
    """
    def __init__(self, path):
        """
        Requires:
        - path: str, the full file path to the existing SWMM model .inp.
        """
        BaseReader.__init__(self, path, endline='[')

        self._title = None
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
        self._outlets = None
        self._weirs = None
        self._xsections = None
        self._curves = None
        self._transects = None
        self._losses = None
        self._timeseries = None
        self._report = None
        self._tags = None
        self._map = None
        self._coordinates = None
        self._vertices = None
        self._polygons = None
        self._symbols = None

        self._not_in_inp = None
        self.cards_in_inp = None

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
            'transects': ('[TRANSECTS]', 2),
            'losses': ('[LOSSES]', 2),
            'timeseries': ('[TIMESERIES]', 2),
            'report': ('[REPORT]', 2),
            'tags': ('[TAGS]', 2),
            'map': ('[MAP]', 2),
            'coordinates': ('[COORDINATES]', 2),
            'vertices': ('[VERTICES]', 2),
            'polygons': ('[Polygons]', 2),
            'symbols': ('[SYMBOLS]', 2),
            # TODO
            # controls
            # snowpacks
            # pollutants
            # loadings
            # patterns
            # washoff
            # treatment
            # pumps
            # hydrographs
            # rdii
            # buildup
            # dwf
            # inflows
            # coverage
            # dividers
            # landuses
        }

        self._check_headers()

    def BlockDoesNotExistWarning(self):
        raise(NotImplementedError)
        # TODO
        # need some error handling when a block
        # is not in the inp.

    def _check_headers(self):
        # check that all of the header blocks are accounted for
        # raise an error if they are not
        # we should consider letter case here as well.
        # consider making a modified file object with title case?

        known_cards = set(self._startlines.keys())

        cards_in_inp = set([_.split(']')[0][1:].lower() for _ in self.orig_file if _[0] == '['])
        self.cards_in_inp = cards_in_inp

        # check if this inp has any cards not mapped
        not_mapped = cards_in_inp.difference(known_cards)
        for card in not_mapped:
            warnings.warn("Card {} currently not supported.".format(card), Warning)        

        # check which cards are not in the inp
        self._not_in_inp = known_cards.difference(cards_in_inp)


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
                self._make_df('options', names))

        return self._options

    @property
    def evaporation(self):
        # this might need special parsing.
        # Can't tell from sample

        if self._evaporation is None:
            names = ['Data_Source', 'Parameters']

            self._evaporation = self._clean_comments(
                self._make_df('evaporation', names))

        return self._evaporation

    @property
    def temperature(self):
        # requires special parsing
        raise(NotImplementedError)
        if self._temperature is None:
            names = ['Data_Element', 'Values']

            self._temperature = self._clean_comments(
                self._make_df('temperature', names))

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
                self._make_df('raingages', names))

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
                self._make_df('subcatchments', names))

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
                self._make_df('subareas', names))

        return self._subareas

    @property
    def infiltration(self):
        if self._infiltration is None:
            names = ['Subcatchment', 'Suction', 'HydCon', 'IMDmax']

            self._infiltration = self._clean_comments(
                self._make_df('infiltration', names))

        return self._infiltration


    @property
    def lid_controls(self):
        raise(NotImplementedError)

        if self._lid_controls is None:
            names = []
            self._lid_controls = self._clean_comments(
                self._make_df('lid_controls', names))

        return self._lid_controls


    @property
    def lid_usage(self):
        raise(NotImplementedError)

        if self._lid_usage is None:
            names = []
            self._lid_usage = self._clean_comments(
                self._make_df('lid_usage', names))

        return self._lid_usage


    @property
    def aquifers(self):
        raise(NotImplementedError)

        if self._aquifers is None:
            names = []
            self._aquifers = self._clean_comments(
                self._make_df('aquifers', names))

        return self._aquifers


    @property
    def groundwater(self):
        raise(NotImplementedError)

        if self._groundwater is None:
            names = []
            self._groundwater = self._clean_comments(
                self._make_df('groundwater', names))

        return self._groundwater


    @property
    def junctions(self):
        if self._junctions is None:
            names = [
                'Name', 'Invert_Elev',
                'Max_Depth', 'Init_Depth',
                'Surcharge_Depth', 'Ponded_Area'
                ]
            self._junctions = self._clean_comments(
                self._make_df('junctions', names))

        return self._junctions


    @property
    def outfalls(self):
        if self._outfalls is None:
            names = [
                'Name', 'Invert_Elev',
                'Outfall_Type', 'Stage_Table_Time_Series',
                'Tide_Gate', 'Route_To'
            ]
            self._outfalls = self._clean_comments(
                self._make_df('outfalls', names, skiprows=1))

        return self._outfalls


    @property
    def storage(self):
        raise(NotImplementedError)

        if self._storage is None:
            names = []
            self._storage = self._clean_comments(
                self._make_df('storage', names))

        return self._storage


    @property
    def conduits(self):
        if self._conduits is None:
            names = [
                'Name', 'Inlet_Node',
                'Outlet_Node', 'Length',
                'Manning_N', 'Inlet_Offset',
                'Outlet_Offset', 'Init_Flow',
                'Max_Flow',
            ]
            self._conduits = self._clean_comments(
                self._make_df('conduits', names))

        return self._conduits


    @property
    def orifices(self):
        raise(NotImplementedError)

        if self._orifices is None:
            names = []
            self._orifices = self._clean_comments(
                self._make_df('orifices', names))

        return self._orifices


    @property
    def outlets(self):
        if self._outlets is None:
            names = [
                'Name', 'Inlet_Node',
                'Outlet_Node', 'Outflow_Height',
                'Outlet_Type', 'Qcoeff_QTable',
                'Qexpon', 'Flap_Gate',
            ]
            self._outlets = self._clean_comments(
                self._make_df('outlets', names))

        return self._outlets


    @property
    def weirs(self):
        if self._weirs is None:
            names = [
                'Name', 'From_Node', 'To_Node', 'Type',
                'CrestHt', 'Qcoeff', 'Gated', 'EndCon',
                'EndCoeff', 'Surcharge', 'RoadWidth', 'RoadSurf'
            ]
            self._weirs = self._clean_comments(
                self._make_df('weirs', names))

        return self._weirs


    @property
    def xsections(self):
        if self._xsections is None:
            names = [
                'Link', 'Shape', 'Geom1',
                'Geom2', 'Geom3', 'Geom4',
                'Barrels'
            ]
            self._xsections = self._clean_comments(
                self._make_df('xsections', names))

        return self._xsections

    @property
    def transects(self):
        raise(NotImplementedError)
        # this will require a special function
        if self._transects is None:
            names = []
            self._transects = self._clean_comments(
                self._make_df('transects', names))

        return self._transects

    @property
    def losses(self):
        if self._losses is None:
            names = [
                'Link', 'Inlet', 'Outlet',
                'Average', 'Flap_Gate', 'SeepageRate'
            ]
            self._losses = self._clean_comments(
                self._make_df('losses', names))

        return self._losses

    @property
    def curves(self):
        if self._curves is None:
            names = ['Name', 'Type', 'X_Value', 'Y_Value']
            self._curves = self._clean_comments(
                self._make_df('curves', names))

        return self._curves


    @property
    def timeseries(self):
        if self._timeseries is None:
            names = ['Name', 'Date', 'Time', 'Value']
            self._timeseries = self._clean_comments(
                self._make_df('timeseries', names))

        return self._timeseries


    @property
    def report(self):
        if self._report is None:
            names = ['Param', 'Value']
            self._report = self._clean_comments(
                self._make_df('report', names))

        return self._report


    @property
    def tags(self):
        raise(NotImplementedError)

        if self._tags is None:
            names = ['Object', 'Name', 'Type']
            self._tags = self._clean_comments(
                self._make_df('tags', names))

        return self._tags


    @property
    def map(self):
        raise(NotImplementedError)
        # requires special function
        if self._map is None:
            names = []
            self._map = self._clean_comments(
                self._make_df('map', names))

        return self._map


    @property
    def coordinates(self):
        if self._coordinates is None:
            names = ['Node', 'X_Coord', 'Y_Coord']
            self._coordinates = self._clean_comments(
                self._make_df('coordinates', names))

        return self._coordinates


    @property
    def vertices(self):
        if self._vertices is None:
            names = ['Link', 'X_Coord', 'Y_Coord']
            self._vertices = self._clean_comments(
                self._make_df('vertices', names))

        return self._vertices


    @property
    def polygons(self):
        if self._polygons is None:
            names = ['Subcatchment', 'X_Coord', 'Y_Coord']
            self._polygons = self._clean_comments(
                self._make_df('polygons', names))

        return self._polygons


    @property
    def symbols(self):
        if self._symbols is None:
            names = ['Gage', 'X_Coord', 'Y_Coord']
            self._symbols = self._clean_comments(
                self._make_df('symbols', names))

        return self._symbols

