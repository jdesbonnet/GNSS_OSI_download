# GNSS_OSI_download

A python script to download GNSS RINEX files from [Tailte Éireann](https://www.tailte.ie/en/)
(formerly Ordnance Survey of Ireland or OSI) Active GNSS Station network.
The data download site is at https://gnss.osi.ie. 
Please agree to terms and conditions on site first.

This script is known to be working as of 2024-11-20.


## Examples

Getting help on command line options:

```
python3 osi_gnss_download.py -h
```

Getting a list of station IDs:

```
python3 osi_gnss_download.py --list-stations
```

Downloading data:

```
python3 osi_gnss_download.py --station-id=glw1 --date=2024-11-19 --start-hour=00 --end-hour=06
```

Data is downloaded as a ZIP archive and saved in format `RINEX_{stnid}_{date}_{start_hour}_{end_hour}.zip`. 
Example: 'RINEX_glw1_2024-11-19_00_06.zip'

