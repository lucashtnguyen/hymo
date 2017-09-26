import pytest
from io import StringIO

import pandas as pd
import pandas.util.testing as pdtest

from lspcreport import LSPCResults
from .utils import data_path

RESULT_STRING = ("""    subbasin  deluid     parmname  value1
0     101174       3         AREA     0.0
1     101174       3         PREC     0.0
2     101174       3         SURO     0.0
3     101174       3         IFWO     0.0
4     101174       3         AGWO     0.0
5     101174       3         PERO     0.0
6     101174       3         TAET     0.0
7     101174       3         IGWI     0.0
8     101174       3       IRRCAN     0.0
9     101174       3       IRRSUR     0.0
10    101174       3       IRRUZS     0.0
11    101174       3       IRRLZS     0.0
12    101174       3       IRRGWS     0.0
13    101174       3      SEDLOAD     0.0
14    101174       3      SEDWSSD     0.0
15    101174       3      SEDSCRS     0.0
16    101174       3      SEDSURO     0.0
17    101174       3      SEDIFWO     0.0
18    101174       3      SEDAGWO     0.0
19    101174       3       SOLIDS     0.0
20    101174       3       SWEPTS     0.0
21    101174       3        SO_TN     0.0
22    101174       3        IO_TN     0.0
23    101174       3        AO_TN     0.0
24    101174       3        PO_TN     0.0
25    101174       3        SO_TP     0.0
26    101174       3        IO_TP     0.0
27    101174       3        AO_TP     0.0
28    101174       3        PO_TP     0.0
29    101174       3       SO_TCU     0.0
30    101174       3       IO_TCU     0.0
31    101174       3       AO_TCU     0.0
32    101174       3       PO_TCU     0.0
33    101174       3      SED_TCU     0.0
34    101174       3  SEDWSSD_TCU     0.0
35    101174       3  SEDSCRS_TCU     0.0
36    101174       3       SO_TPB     0.0
37    101174       3       IO_TPB     0.0
38    101174       3       AO_TPB     0.0
39    101174       3       PO_TPB     0.0
40    101174       3      SED_TPB     0.0
41    101174       3  SEDWSSD_TPB     0.0
42    101174       3  SEDSCRS_TPB     0.0
43    101174       3       SO_TZN     0.0
44    101174       3       IO_TZN     0.0
45    101174       3       AO_TZN     0.0
46    101174       3       PO_TZN     0.0
47    101174       3      SED_TZN     0.0
48    101174       3  SEDWSSD_TZN     0.0
49    101174       3  SEDSCRS_TZN     0.0
50    101174       3     SO_FECAL     0.0
51    101174       3     IO_FECAL     0.0
52    101174       3     AO_FECAL     0.0
53    101174       3     PO_FECAL     0.0
54    101174       3     SO_Total     0.0
55    101174       3     IO_Total     0.0
56    101174       3     AO_Total     0.0
57    101174       3     PO_Total     0.0
58    101174       3    SO_Entero     0.0
59    101174       3    IO_Entero     0.0
60    101174       3    AO_Entero     0.0
61    101174       3    PO_Entero     0.0""")

SUMMARY_STRING = ("""TT-----------------------------------------------------------------------------------------
TT LSPC -- Loading Simulation Program, C++
TT Version 5.0 - October 10, 2015
TT
TT Designed and maintained by:
TT     Tetra Tech, Inc.
TT     10306 Eaton Place, Suite 340
TT     Fairfax, VA 22030
TT     (703) 385-6000
TT-----------------------------------------------------------------------------------------
TT LSPC MODEL LANDUSE SUMMARY HEADER FILE
TT This header file was created at 03:21:14pm on 08/28/2017
TT Output start time:  10/1/2002
TT Output end time:    9/30/2003
TT Simulation time step:   60 min
TT Label   
TT AREA     average area (acre)
TT PREC     total precipitation (rain + snow) volume (in-acre/year) 
TT SURO     total surface outflow rate volume (in-acre/year) 
TT IFWO     total interflow outflow rate volume (in-acre/year) 
TT AGWO     total groundwater outflow rate volume (in-acre/year) 
TT PERO     total outflow rate volume (in-acre/year) 
TT TAET     total actual evapo-transpiration volume (in-acre/year) 
TT IGWI     total groundwater deep percolation volume (in-acre/year) 
TT IRRCAN     irrigation requirement applied over the canopy (in-acre/year) 
TT IRRSUR     irrigation water applied directly to the soil surface (in-acre/year) 
TT IRRUZS     irrigation water applied to the upper soil zone via buried systems (in-acre/year) 
TT IRRLZS     irrigation water likewise applied to the lower soil zone (in-acre/year) 
TT IRRGWS     irrigation water entering directly into the local groundwater, such as seepage irrigation (in-acre/year) 
TT SEDLOAD  sediments load from land (tons/year) 
TT SEDWSSD  sediments load from land (tons/year)
TT SEDSCRS  sediments load from land (tons/year)
TT SEDSURO  sediments load from land (tons/year)
TT SEDIFWO  sediments load from land (tons/year)
TT SEDAGWO  sediments load from land (tons/year)
TT SOLIDS   sediments in surface storage on the land (tons/year)
TT SWEPTS   sediments swept from surface storage on the land (tons/year)
TT SO_TN surface flux of QUAL TN (lb/year) 
TT IO_TN interflow flux of QUAL TN (lb/year) 
TT AO_TN groundwater flux of QUAL TN (lb/year) 
TT PO_TN total flux of QUAL TN (lb/year) 
TT SO_TP surface flux of QUAL TP (lb/year) 
TT IO_TP interflow flux of QUAL TP (lb/year) 
TT AO_TP groundwater flux of QUAL TP (lb/year) 
TT PO_TP total flux of QUAL TP (lb/year) 
TT SO_TCU surface flux of QUAL TCU (lb/year) 
TT IO_TCU interflow flux of QUAL TCU (lb/year) 
TT AO_TCU groundwater flux of QUAL TCU (lb/year) 
TT PO_TCU total flux of QUAL TCU (lb/year) 
TT SED_TCU total flux of sediment associated QUAL TCU (lb/year) 
TT SEDWSSD_TCU total flux of sediment associated QUAL TCU (lb/year) 
TT SEDSCRS_TCU total flux of sediment associated QUAL TCU (lb/year) 
TT SO_TPB surface flux of QUAL TPB (lb/year) 
TT IO_TPB interflow flux of QUAL TPB (lb/year) 
TT AO_TPB groundwater flux of QUAL TPB (lb/year) 
TT PO_TPB total flux of QUAL TPB (lb/year) 
TT SED_TPB total flux of sediment associated QUAL TPB (lb/year) 
TT SEDWSSD_TPB total flux of sediment associated QUAL TPB (lb/year) 
TT SEDSCRS_TPB total flux of sediment associated QUAL TPB (lb/year) 
TT SO_TZN surface flux of QUAL TZN (lb/year) 
TT IO_TZN interflow flux of QUAL TZN (lb/year) 
TT AO_TZN groundwater flux of QUAL TZN (lb/year) 
TT PO_TZN total flux of QUAL TZN (lb/year) 
TT SED_TZN total flux of sediment associated QUAL TZN (lb/year) 
TT SEDWSSD_TZN total flux of sediment associated QUAL TZN (lb/year) 
TT SEDSCRS_TZN total flux of sediment associated QUAL TZN (lb/year) 
TT SO_FECAL surface flux of QUAL FECAL (#/year) 
TT IO_FECAL interflow flux of QUAL FECAL (#/year) 
TT AO_FECAL groundwater flux of QUAL FECAL (#/year) 
TT PO_FECAL total flux of QUAL FECAL (#/year) 
TT SO_Total surface flux of QUAL Total (#/year) 
TT IO_Total interflow flux of QUAL Total (#/year) 
TT AO_Total groundwater flux of QUAL Total (#/year) 
TT PO_Total total flux of QUAL Total (#/year) 
TT SO_Entero surface flux of QUAL Entero (#/year) 
TT IO_Entero interflow flux of QUAL Entero (#/year) 
TT AO_Entero groundwater flux of QUAL Entero (#/year) 
TT PO_Entero total flux of QUAL Entero (#/year) 
TT
TT     This is header file for the landuse summary file landuse.csv
"""
)

class Test_LSPCResults(object):
    def setup(self):

        self.known_results_path = data_path('landuse.csv')
        self.known_summary_path = data_path('landuse.out')
        self.known_summary_EOF = -2

        self.known_results = pd.read_csv(
            StringIO(RESULT_STRING), delim_whitespace=True)

        self.known_raw_summary = SUMMARY_STRING

        self.known_parsed_summary = pd.read_csv(
            data_path('known_summary.csv'), index_col=[0])

        self.known_parsed_results = pd.read_csv(
            data_path('known_parsed_results.csv'))

        self.lspc = LSPCResults(self.known_results_path,
                                 self.known_summary_path,
                                 self.known_summary_EOF)
        
    def teardown(self):
        None

    def test_results_path(self):
        assert self.known_results_path == self.lspc.results_path

    def test_summary_path(self):
        assert self.known_summary_path == self.lspc.summary_path

    def test_summary_EOF(self):
        with pytest.raises(ValueError):
            LSPCResults(self.known_results_path,
                        self.known_summary_path,
                        1)
        with pytest.raises(ValueError):
            LSPCResults(self.known_results_path,
                        self.known_summary_path,
                        -1.1)

        assert self.known_summary_EOF == self.lspc._summary_EOF

    def test_raw_results(self):
        pdtest.assert_frame_equal(
            self.known_results, self.lspc.raw_results)

    def test_raw_summary(self):
        assert self.known_raw_summary == self.lspc.raw_summary

    def test_parsed_summary(self):
        pdtest.assert_frame_equal(
            self.known_parsed_summary, self.lspc.parsed_summary)

    def test_parsed_results(self):
        pdtest.assert_frame_equal(
            self.known_parsed_results, self.lspc.parsed_results)