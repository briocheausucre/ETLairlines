from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd


class FlightsExtractor():
    def __init__(self, icaos, to_csv=True, update=True, from_icao=False):
        self.api = OpenSkyApi()
        self.username = 'Hippolyte'
        self.password = 'dyqXex-tajwij-fuzpa7'
        if from_icao:
            self.start_timestamp = int((datetime.now() - timedelta(days=30)).timestamp())
        else:
            self.start_timestamp = int((datetime.now() - timedelta(hours=2)).timestamp())
        self.end_timestamp = int(datetime.now().timestamp())
        if update:
            if from_icao:
                self.df = self.get_data(icaos)
            else:
                self.df = self.get_data()

        else:
            self.df = pd.read_csv('Data/flights.csv')
        if to_csv:
            self.to_csv()

    def get_data(self, icaos=None):
        df = pd.DataFrame(columns=['icao','totaldist','totaltime'])
        airports = pd.read_csv('Data/airports.csv')
        if icaos == None:
            icaos = []
            flights = self.api.get_flights_from_interval(self.start_timestamp, self.end_timestamp)
            if flights != None:
                total_distance = 0
                total_flighttime = 0
                for flight in flights:
                    icao = flight.icao24
                    if (icao not in icaos) and self._are_airports_valid(airports, flight):
                        distance, flighttime = self._get_data(airports, flight)
                        total_distance += distance
                        total_flighttime += flighttime
                        icaos.append(icao)
                        new_row = {'icao': icao, 'totaldist': total_distance, 'totaltime': total_flighttime}
                        df.loc[len(df)] = new_row
        else:
            for icao in icaos:
                url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao}&begin={self.start_timestamp}&end={self.end_timestamp}"
                response = requests.get(url, auth=(self.username, self.password))
                if response.status_code != 429:
                    flights = response.json()
                    total_distance = 0
                    total_flighttime = 0
                    for flight in flights:
                        distance, flighttime = self._get_data(airports, flight)
                        total_distance += distance
                        total_flighttime += flighttime
                    new_row = {'icao': icao, 'totaldist': total_distance, 'totaltime': total_flighttime}
                    df.loc[len(df)] = new_row
        if len(df) == 0:
            df = pd.read_csv('Data/flights.csv')
        return df
    
    def _get_data(self, airports, flight):
        dep_airport = flight.estDepartureAirport
        arv_airport = flight.estArrivalAirport
        lat_dep = airports[airports['icao']==dep_airport]['lat'].values[0]
        long_dep = airports[airports['icao']==dep_airport]['long'].values[0]
        lat_arv = airports[airports['icao']==arv_airport]['lat'].values[0]
        long_arv = airports[airports['icao']==arv_airport]['long'].values[0]
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(np.radians, [lat_dep, long_dep, lat_arv, long_arv])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
        dep_time = flight.firstSeen
        arv_time = flight.lastSeen
        return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)), arv_time - dep_time
    
    def _are_airports_valid(self, airports, flight):
        dep_airport = flight.estDepartureAirport
        arv_airport = flight.estArrivalAirport
        if dep_airport is None:
            return False
        if arv_airport is None:
            return False
        if len(airports[airports['icao']==dep_airport]['lat'].values) == 0:
            return False
        if len(airports[airports['icao']==dep_airport]['long'].values) == 0:
            return False
        if len(airports[airports['icao']==arv_airport]['lat'].values) == 0:
            return False
        if len(airports[airports['icao']==arv_airport]['long'].values) == 0:
            return False
        return True

    def to_csv(self):
        self.df.to_csv('Data/flights.csv', index=False)

    def to_database(self):
        '''
        Uploads the flights dataset to the SQL online database
        '''
        pass


if __name__ == '__main__':
    ae = FlightsExtractor(['3c675a'])
    print(ae.df.head())