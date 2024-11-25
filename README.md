# GNSS_OSI_download

A python script to download GNSS RINEX files from [Tailte Éireann](https://www.tailte.ie/en/)
(formerly Ordnance Survey of Ireland or OSI) Active GNSS Station network.
The data download site is at https://gnss.osi.ie. 
Before downloading data, please agree to terms and conditions at https://gnss.osi.ie first. 
This software is covered by the MIT License.

This script is known to be working as of 2024-11-20.

Note: it seems only the last 30 days of data can be downloaded.



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



## Dependencies

This script makes use of the requests and BeautifulSoup packages. On Ubuntu 22.04 these can be installed
with the following command:

```
sudo apt-get install python3-requests python3-bs4
```



## Command line options

```
usage: osi_gnss_download.py [-h] [--list-stations] --station-id STATION_ID
                            --date DATE [--start-hour START_HOUR]
                            [--end-hour END_HOUR] [--user-agent USER_AGENT]

Download GNSS RINEX files from https://gnss.osi.ie. Please agree to T&C on
site first.

optional arguments:
  -h, --help            show this help message and exit
  --list-stations       Obtain a list of station IDs and exit. (default:
                        False)
  --station-id STATION_ID
                        Station ID. Use --list-stations to obtain an
                        exhaustive list. Example glw1 (Galway) (default: None)
  --date DATE           Date of data capture yyyy-mm-dd (default: None)
  --start-hour START_HOUR
                        Start hour (UTC) 0 to 22 (default: 0)
  --end-hour END_HOUR   End hour (UTC) 1 to 23 (default: 24)
  --user-agent USER_AGENT
                        User-agent header to use in transaction (default:
                        GNSS_OSI_download v1.0)

```
