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
        self.icaos = self.df['icao'].unique().tolist()

    def get_data(self, icaos=None):
        df = pd.DataFrame(columns=['icao','totaldist','totaltime'])
        if icaos == None:
            icaos = []
            flights = self.api.get_flights_from_interval(self.start_timestamp, self.end_timestamp)
            if flights != None:
                total_distance = 0
                total_flighttime = 0
                for flight in flights:
                    icao = flight.icao24
                    if (icao not in icaos) and self._are_airports_valid(flight):
                        distance, flighttime = self._get_data(flight)
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
                        distance, flighttime = self._get_data(flight)
                        total_distance += distance
                        total_flighttime += flighttime
                    new_row = {'icao': icao, 'totaldist': total_distance, 'totaltime': total_flighttime}
                    df.loc[len(df)] = new_row
        if len(df) == 0:
            df = pd.read_csv('Data/flights.csv')
        return df
    
    def _get_data(self, flight):
        hor_dist_dep = flight.estDepartureAirportHorizDistance
        ver_dist_dep = flight.estDepartureAirportVertDistance
        hor_dist_arv = flight.estArrivalAirportVertDistance
        ver_dist_arv = flight.estArrivalAirportVertDistance
        dep_time = flight.firstSeen
        arv_time = flight.lastSeen
        return np.sqrt((hor_dist_dep - hor_dist_arv)**2 + (ver_dist_dep - ver_dist_arv)**2), arv_time - dep_time
    
    def _are_airports_valid(self, flight):
        dep_airport = flight.estDepartureAirport
        if dep_airport is None:
            return False
        return True
    
    def transform(self, icaos):
        self.df = self.df[self.df['icao'].isin(icaos)]
        self.icaos = self.df['icao'].unique().tolist()

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