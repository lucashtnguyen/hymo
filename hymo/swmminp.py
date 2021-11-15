import pandas as pd
import numpy as np

from .base_reader import BaseReader


class SWMMInpFile(BaseReader):
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
        self._dividers = None
        self._conduits = None
        self._orifices = None
        self._outlets = None
        self._weirs = None
        self._pumps = None
        self._xsections = None
        self._pollutants = None
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
        self._inflows = None

        self._not_in_inp = None
        self.cards_in_inp = None
        self.not_mapped = set()

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
            'temperature': ('[TEMPERATURE]', 2),  # requires special parsing
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
            'dividers': ('[DIVIDERS]', 2),
            'conduits': ('[CONDUITS]', 2),
            'orifices': ('[ORIFICES]', 2),
            'outlets': ('[OUTLETS]', 2),
            'weirs': ('[WEIRS]', 2),
            'pumps': ('[PUMPS]', 2),
            'xsections': ('[XSECTIONS]', 2),
            'curves': ('[CURVES]', 2),
            'transects': ('[TRANSECTS]', 2),
            'losses': ('[LOSSES]', 2),
            'timeseries': ('[TIMESERIES]', 2),
            'report': ('[REPORT]', 2),
            'tags': ('[TAGS]', 1),
            'map': ('[MAP]', 2),
            'coordinates': ('[COORDINATES]', 2),
            'vertices': ('[VERTICES]', 2),
            'polygons': ('[Polygons]', 2),
            'symbols': ('[SYMBOLS]', 2),
            'pollutants': ('[POLLUTANTS]', 2),
            'inflows': ('[INFLOWS]', 2)
            # TODO
            # controls
            # snowpacks
            # loadings
            # patterns
            # washoff
            # treatment
            # pumps # added minimum required info for flow network
            # hydrographs
            # rdii
            # buildup
            # dwf
            # coverage
            # dividers # added minimum required info for flow network
            # landuses
        }

        self._check_headers()

    def __getattr__(self, name):
        if name in self.not_mapped:
            raise NotImplementedError("Card {} currently not supported.".format(name))
        else:  
            raise AttributeError(name)

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
            if l.lower().find(line.lower()) > -1:
                break
        return n

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

        cards_in_inp = set([_.split(']')[0][1:].lower()
                            for _ in self.orig_file if _[0] == '['])
        self.cards_in_inp = cards_in_inp

        # check if this inp has any cards not mapped
        self.not_mapped = cards_in_inp.difference(known_cards)

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

            self._options = (
                self._make_df('options', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._options

    @property
    def evaporation(self):
        # this might need special parsing.
        # Can't tell from sample

        if self._evaporation is None:
            names = ['Data_Source', 'Parameters']

            self._evaporation = (
                self._make_df('evaporation', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._evaporation

    @property
    def temperature(self):
        # requires special parsing
        raise(NotImplementedError)
        if self._temperature is None:
            names = ['Data_Element', 'Values']

            self._temperature = (
                self._make_df('temperature', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._temperature

    @property
    def raingages(self):
        if self._raingages is None:
            names = [
                'Name', 'Format',
                'Interval', 'SCF',
                'Source', 'Path'
            ]

            dtype = {
                'Name': str,
            }

            self._raingages = (
                self._make_df('raingages', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

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

            dtype = {
                'Name': str,
                'Rain_Gage': str,
                'Outlet': str,
            }

            self._subcatchments = (
                self._make_df('subcatchments', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

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

            dtype = {
                'Subcatchment': str,
                'RouteTo': str,
            }

            self._subareas = (
                self._make_df('subareas', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._subareas

    @property
    def infiltration(self):
        if self._infiltration is None:
            names = ['Subcatchment', 'Suction', 'HydCon', 'IMDmax']

            dtype = {
                'Subcatchment': str,
            }

            self._infiltration = (
                self._make_df('infiltration', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._infiltration

    @property
    def lid_controls(self):
        raise(NotImplementedError)

        if self._lid_controls is None:
            names = []
            self._lid_controls = (
                self._make_df('lid_controls', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._lid_controls

    @property
    def lid_usage(self):
        raise(NotImplementedError)

        if self._lid_usage is None:
            names = []
            self._lid_usage = (
                self._make_df('lid_usage', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._lid_usage

    @property
    def aquifers(self):
        raise(NotImplementedError)

        if self._aquifers is None:
            names = []
            self._aquifers = (
                self._make_df('aquifers', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._aquifers

    @property
    def groundwater(self):
        raise(NotImplementedError)

        if self._groundwater is None:
            names = []
            self._groundwater = (
                self._make_df('groundwater', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._groundwater

    @property
    def junctions(self):
        if self._junctions is None:
            names = [
                'Name', 'Invert_Elev',
                'Max_Depth', 'Init_Depth',
                'Surcharge_Depth', 'Ponded_Area'
            ]

            dtype = {
                'Name': str,
            }

            self._junctions = (
                self._make_df('junctions', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._junctions

    @property
    def outfalls(self):
        if self._outfalls is None:
            names = [
                'Name', 'Invert_Elev',
                'Outfall_Type', 'Stage_Table_Time_Series',
                'Tide_Gate', 'Route_To'
            ]

            dtype = {
                'Name': str,
                'Outfall_Type': str,
            }

            self._outfalls = (
                self._make_df('outfalls', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._outfalls

    @property
    def storage(self):
        # raise(NotImplementedError)

        if self._storage is None:
            names = [
                'Name', 'Invert_Elev', 'Max_Depth',
                'Init_Depth', 'Storage_Curve',
            ]

            dtype = {
                'Name': str,
                'Invert_Elev': str,
                'Max_Depth': str,
                'Init_Depth': str,
                'Storage_Curve': str,
            }

            self._storage = (
                self._make_df('storage', comment=';', sep='\s+', header=None,
                              names=names, usecols=range(5),
                              index_col=[0], dtype=dtype))

        return self._storage

    @property
    def dividers(self):
        # raise(NotImplementedError)

        if self._dividers is None:
            names = [
                'Name', 'Elevation', 'Diverted_Link', 'Type',
            ]

            dtype = {
                'Name': str,
                'Elevation': str,
                'Diverted_Link': str,
                'Type': str,
            }
            self._dividers = (
                self._make_df('dividers', comment=';', sep='\s+', header=None,
                              names=names, usecols=range(4),
                              index_col=[0], dtype=dtype))

        return self._dividers

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

            dtype = {
                'Name': str,
                'Inlet_Node': str,
                'Outlet_Node': str
            }

            self._conduits = (
                self._make_df('conduits', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._conduits

    @property
    def orifices(self):
        # raise(NotImplementedError)

        if self._orifices is None:
            names = [
                'Name', 'From_Node', 'To_Node', 'Type', 'Offset',
                'Qcoeff', 'Gated', 'CloseTime']

            dtype = {
                'Name': str,
                'From_Node': str,
                'To_Node': str,
                'Type': str
            }

            self._orifices = (
                self._make_df('orifices', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

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

            dtype = {
                'Name': str,
                'Inlet_Node': str,
                'Outlet_Node': str
            }

            self._outlets = (
                self._make_df('outlets', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._outlets

    @property
    def weirs(self):
        if self._weirs is None:
            names = [
                'Name', 'From_Node', 'To_Node', 'Type',
                'CrestHt', 'Qcoeff', 'Gated', 'EndCon',
                'EndCoeff', 'Surcharge', 'RoadWidth', 'RoadSurf'
            ]

            dtype = {
                'Name': str,
                'From_Node': str,
                'To_Node': str,
                'Type': str
            }

            self._weirs = (
                self._make_df('weirs', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._weirs

    @property
    def pumps(self):
        if self._pumps is None:
            names = [
                'Name', 'From_Node', 'To_Node',
            ]

            dtype = {
                'Name': str,
                'From_Node': str,
                'To_Node': str,
            }

            self._pumps = (
                self._make_df('pumps', comment=';', sep='\s+', header=None,
                              names=names, usecols=range(3),
                              index_col=[0], dtype=dtype))

        return self._pumps

    @property
    def xsections(self):
        if self._xsections is None:
            names = [
                'Link', 'Shape', 'Geom1',
                'Geom2', 'Geom3', 'Geom4',
                'Barrels'
            ]

            dtype = {
                'Link': str,
            }

            self._xsections = (
                self._make_df('xsections', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._xsections

    @property
    def transects(self):
        raise(NotImplementedError)
        # this will require a special function
        if self._transects is None:
            names = []
            self._transects = (
                self._make_df('transects', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._transects

    @property
    def losses(self):
        if self._losses is None:
            names = [
                'Link', 'Inlet', 'Outlet',
                'Average', 'Flap_Gate', 'SeepageRate'
            ]

            dtype = {
                'Link': str,
                'Inlet': str,
                'Outlet': str,
            }
            self._losses = (
                self._make_df('losses', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._losses

    @property
    def curves(self):
        if self._curves is None:
            names = ['Name', 'Type', 'X_Value', 'Y_Value']
            dtype = {'Name': str}

            df_raw = (
                self._make_df('curves', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

            df = (df_raw.assign(_Y_Value=lambda df: np.where(df.Y_Value.isnull(), df.X_Value, df.Y_Value))
                .assign(_X_Value=lambda df: np.where(df.Y_Value.isnull(), df.Type, df.X_Value))
                .assign(_Type=lambda df: np.where(df.Y_Value.isnull(), np.nan, df.Type))
                .loc[:, ['_Type', '_X_Value', '_Y_Value']]
                .rename(columns=lambda s: s.strip('_'))
            )
            self._curves = df

        return self._curves

    @property
    def timeseries(self):
        if self._timeseries is None:
            names = ['Name', 'Date', 'Time', 'Value']
            dtype = {'Name': str}
            self._timeseries = (
                self._make_df('timeseries', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._timeseries

    @property
    def report(self):
        if self._report is None:
            names = ['Param', 'Value']
            self._report = (
                self._make_df('report', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._report

    @property
    def tags(self):

        if self._tags is None:
            names = ['Object', 'Name', 'Type']
            dtype = {'Name': str}
            self._tags = (
                self._make_df('tags', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._tags

    @property
    def map(self):
        raise(NotImplementedError)
        # requires special function
        if self._map is None:
            names = []
            self._map = (
                self._make_df('map', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0]))

        return self._map

    @property
    def coordinates(self):
        if self._coordinates is None:
            names = ['Node', 'X_Coord', 'Y_Coord']
            dtype = {
                'Node': str,
                'X_Coord': np.float64,
                'Y_Coord': np.float64,
            }
            self._coordinates = (
                self._make_df('coordinates', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._coordinates

    @property
    def vertices(self):
        if self._vertices is None:
            names = ['Link', 'X_Coord', 'Y_Coord']
            dtype = {
                'Link': str,
                'X_Coord': np.float64,
                'Y_Coord': np.float64,
            }
            self._vertices = (
                self._make_df('vertices', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._vertices

    @property
    def polygons(self):
        if self._polygons is None:
            names = ['Subcatchment', 'X_Coord', 'Y_Coord']

            dtype = {
                'Subcatchment': str,
                'X_Coord': np.float64,
                'Y_Coord': np.float64,
            }

            self._polygons = (
                self._make_df('polygons', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._polygons

    @property
    def symbols(self):
        if self._symbols is None:
            names = ['Gage', 'X_Coord', 'Y_Coord']
            dtype = {'Gage': str}
            self._symbols = (
                self._make_df('symbols', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._symbols

    @property
    def pollutants(self):
        if self._pollutants is None:
            names = ['Name', 'Units', 'Crain', 'Cgw',
                     'Crdii', 'Kdecay', 'SnowOnly',
                     'Co_Pollutant', 'Co_Frac', 'Cdwf', 'Cinit']
            dtype = {'Name': str}
            self._pollutants = (
                self._make_df('pollutants', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._pollutants

    @property
    def inflows(self):
        if self._inflows is None:
            names = ['Node', 'Constituent', 'Time_Series', 'Type',
            'Mfactor', 'Sfactor', 'Baseline', 'Pattern']
            dtype = {'Node': str}
            self._inflows = (
                self._make_df('inflows', comment=';', sep='\s+', header=None,
                              names=names, index_col=[0], dtype=dtype))

        return self._inflows
