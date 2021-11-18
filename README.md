# hymo
hymo: A Hydro Model reader.

The `BaseReader` class of hymo is an extensible framework to
several different card based model input and output files.


`hymo` merges `swmmreport` and `lspcreport`.
`swmmreport` was previously at (https://github.com/lucashtnguyen/swmmreport)
`lspcreport` was previously at (https://github.com/lucashtnguyen/lspcreport)

# Reading SWMM Based Files

Use the following classes to load SWMM's input and report file: 
```python
import hymo

inp = hymo.SWMMInpFile('example.inp')
rpt = hymo.SWMMReportFile('example.rpt')
```

Most cards in SWMM's input file are supported as class methods, e.g.:
```python
inp.conduits.head()
```
```
Name	Inlet_Node	Outlet_Node	Length	Manning_N	Inlet_Offset	Outlet_Offset	Init_Flow	Max_Flow
135524	18H3-004C	18H3-014C	445.0	0.013	448.3	447.7	0	0.0
135524a	18H3-014C	18H3-605C	675.0	0.013	447.7	446.6	0	0.0
135525	18H1-366C	18H4-105C	280.0	0.013	449.32	448.88	0	0.0
135525a	18H4-105C	18H3-004C	455.0	0.013	448.88	448.3	0	0.0
135527a	18H1-143C	18H1-366C	510.0	0.013	450.01	449.32	0	0.0
```

All cards in the report file are supported, e.g.:
```python
rpt.node_inflow_results.head()
```
```
Node	Type	Maximum_Lateral_Inflow_CFS	Maximum_Total_Inflow_CFS	Time_of_Max_Occurrence_days	Time_of_Max_Occurrence_hours	Lateral_Inflow_Volume_mgals	Total_Inflow_Volume_mgals	Flow_Balance_Error_Percent	flag
13S	JUNCTION	0.0	0.81	0	14:32	0.0	0.479	0.034	
14S	JUNCTION	0.0	0.81	0	14:32	0.0	0.479	0.013	
17H4-0238D	JUNCTION	0.0	102.7	0	04:32	0.0	18.0	0.009	
17J4-049C	JUNCTION	0.0	9.31	0	05:51	0.0	0.952	0.073	
17K3-047C	JUNCTION	2.32	17.39	0	05:51	0.22	1.65	-0.068	

```

[![Build Status](https://travis-ci.org/lucashtnguyen/hymo.svg?branch=master)](https://travis-ci.org/lucashtnguyen/hymo)
[![Coverage Status](https://coveralls.io/repos/lucashtnguyen/hymo/badge.svg?branch=master)](https://coveralls.io/r/lucashtnguyen/hymo?branch=master)