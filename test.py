from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import requests


api = OpenSkyApi()
start_timestamp = int((datetime.now() - timedelta(days=30)).timestamp())
end_timestamp = int(datetime.now().timestamp())

username = 'Hippolyte'
password = 'dyqXex-tajwij-fuzpa7'
#data = api.get_flights_by_aircraft('3c675a', start_timestamp, end_timestamp)
#print(data)
icao = '3c675a'
url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao}&begin={start_timestamp}&end={end_timestamp}"
#response = requests.get(url, auth=(username, password))
#if response.status_code != 429:
#    data = response.json()
#else:
#    print("error")
#for flight in data:
#    print(flight)


flight_data = {
    'arrivalAirportCandidatesCount': 0,
    'callsign': 'LNK621D ',
    'departureAirportCandidatesCount': 22,
    'estArrivalAirport': 'FASX',
    'estArrivalAirportHorizDistance': 4145,
    'estArrivalAirportVertDistance': 6886,
    'estDepartureAirport': 'FACT',
    'estDepartureAirportHorizDistance': 2256,
    'estDepartureAirportVertDistance': 30,
    'firstSeen': 1728365085,
    'icao24': '008081',
    'lastSeen': 1728366165
}

# Accéder à la valeur associée à la clé 'icao24'
icao24_value = flight_data['icao24']

# Afficher la valeur
print(icao24_value)