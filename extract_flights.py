from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


class FlightsExtractor():
    def __init__(self, icaos, to_csv=True, update=True, from_icao=False):
        #self.api = OpenSkyApi()
        self.username = 'Hippolyte'
        self.password = 'dyqXex-tajwij-fuzpa7'
        self.start_timestamp30d = int((datetime.now() - timedelta(days=30)).timestamp())
        self.start_timestamp2hr = int((datetime.now() - timedelta(hours=2)).timestamp())
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
            flights = self.api.get_flights_from_interval(self.start_timestamp2hr, self.end_timestamp)
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
                url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao}&begin={self.start_timestamp30d}&end={self.end_timestamp}"
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
        dep_time = flight.firstSeen
        arv_time = flight.lastSeen
        return hor_dist_dep, arv_time - dep_time
    
    def _are_airports_valid(self, flight):
        dep_airport = flight.estDepartureAirport
        if dep_airport is None:
            return False
        return True
    
    def transform(self, icaos, CO2perkm):
        self.df = self.df[self.df['icao'].isin(icaos)].reset_index(drop=True)
        self.icaos = self.df['icao'].unique().tolist()
        self.df['kgCO2'] = (self.df['totaldist'] / 1000 + 95) * CO2perkm

    def to_csv(self):
        self.df.to_csv('Data/flights.csv', index=False)

    def to_database(self, db_url):
        '''
        Uploads the flights dataset to the SQL online database
        '''
        table_name = 'flights'
        engine = create_engine(db_url)
        with engine.connect() as connection:
            try:
                self.df.to_sql(table_name, con=connection, if_exists='append', index=False)
                print(f"Data loaded successfully into {table_name}")
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                connection.close()