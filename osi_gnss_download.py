import argparse
import requests
from bs4 import BeautifulSoup

#
# Script to download RINEX files from https://gnss.osi.ie
# Note: please agree to terms at https://gnss.osi.ie site before downloading data.
# This software is licenced under the MIT License.
# Joe Desbonnet 2024-11-15
#
# Dependencies:
# * requests to allow HTTP GET/POST with session cookie support.
# * bs4 (BeautifulSoup) to allow parsing of HTML forms to extract hidden session 
#   token and to discover station IDs from SELECT element.
#

# Base URL for the download website
BASE_URL = "https://gnss.osi.ie" 
FORM_ENDPOINT = f"{BASE_URL}/" 
DOWNLOAD_ENDPOINT = f"{BASE_URL}/?download"
DEFAULT_AGENT="GNSS_OSI_download v1.0"
AGENT = {
    'User-Agent': DEFAULT_AGENT
}

def output_response_info (session, response) :
    print("Request Headers:")
    print(response.request.headers)
    print("\nResponse Status Code:", response.status_code)
    print("Response Cookies:", session.cookies.get_dict())
    print("Response Headers:")
    print(response.headers)
    print("\n----")


def list_stations() :
    # Station IDs are embedded in the SELECT element on the download form.
    session = requests.Session()
    response = session.get(FORM_ENDPOINT, headers=AGENT)
    #output_response_info (session,response)
    if response.status_code != 200:
        print(f"Failed to access the home page at {FORM_ENDPOINT}. Status code: {response.status_code}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    station_list = soup.find('select', {'name': 'station0'})
    options = station_list.find_all('option')
    
    # Print station IDs and names from the SELECT element
    for option in options:
        value = option.get('value')
        label = option.text.strip()
        print(f"{value} {label}")



def download_data(station_id, date, start, end):

    
    # Start a session to maintain cookies
    session = requests.Session()
    
    #
    # Step 1: Access the home page to initiate the session
    #
    response = session.get(FORM_ENDPOINT, headers=AGENT)
    #output_response_info (session,response)
    if response.status_code != 200:
        print(f"Failed to access the download home page at {FORM_ENDPOINT}. Status code: {response.status_code}")
        return
    
    # Extracting hidden form field 'as_sfid'
    soup = BeautifulSoup(response.text, 'html.parser')
    hidden_field = soup.find('input', {'name': 'as_sfid'})
    if not hidden_field or not hidden_field.get('value'):
        print("Error: 'as_sfid' hidden field not found in the form.")
        return
    as_sfid = hidden_field['value']


    #
    # Step 2: Submit the form with the filter parameters (station, date, hour(s))
    #
    form_data = {
        'station0': station_id,
        'date': date,
        'start': start,
        'end':end,
        'submitSearchByStation': 'FIND DATA',
        'as_sfid': as_sfid
    }
    response = session.post(FORM_ENDPOINT, data=form_data, headers=AGENT)
    #output_response_info(session,response)
    if response.status_code != 200:
        print(f"Failed to submit the form. Status code: {response.status_code}")
        return
    
    #
    # Step 3: Trigger the data download
    #
    response = session.get(DOWNLOAD_ENDPOINT, headers=AGENT)
    if response.status_code == 200:
        filename = f"RINEX_{station_id}_{date}_{start:02d}_{end:02d}.zip"
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Data successfully downloaded and saved as {filename}")
    else:
        print(f"Failed to download data. Status code: {response.status_code}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Download GNSS RINEX files from https://gnss.osi.ie. Please agree to T&C on site first.",
        epilog="Project website: https://github.com/jdesbonnet/GNSS_OSI_download",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("--list-stations", action="store_true", help="Obtain a list of station IDs and exit.")
    parser.add_argument("--station-id", help="Station ID. Use --list-stations to obtain an exhaustive list. Example glw1 (Galway)", required=True)
    parser.add_argument("--date",help="Date of data capture yyyy-mm-dd", required=True)
    parser.add_argument("--start-hour",help="Start hour (UTC) 0 to 22", default="0")
    parser.add_argument("--end-hour", help="End hour (UTC) 1 to 23", default="24")
    parser.add_argument("--user-agent", help="User-agent header to use in transaction", default=DEFAULT_AGENT)

    args = parser.parse_args()

    # Option to list station IDs and exit
    if args.list_stations :
        list_stations()
        exit()

    # Proceed to data download...
    start = int(args.start_hour)
    if args.end_hour :
        end = int(args.end_hour)
    else :
        end = start + 1

    download_data(args.station_id, args.date, start, end)

