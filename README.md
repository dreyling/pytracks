# pytracks

for analysing n-tuple ROOT output from EUTelescope

## Requirements

Python 2.7 and uproot: ```pip install uproot``` (as sudo if system python)

For a clean environment, use a Miniconda2 installation and 
```conda install numpy && pip install uproot```

## Execution

For inspecting a root-file. Output are the names of ttree and names of leaves:
```python inspect_file.py file.root```

Reading the Tracks and Hits collection and do some checks: Array length, check events with multiple tracks, calculate multiplicity, find duplicated tracks, apply chi2 cut and find tracks having a DUT hit within a given distance cut:
```python read_track.py file.root```
