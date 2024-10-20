from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import requests
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import psycopg2


class FlightsExtractor():
    """
        Classe pour extraire, transformer et load le dataset "flights".

        Paramètres:

        icaos (list): Liste des icaos présents dans le dataset "aircrafts". Le dataset "flights" est
        construit à partir de ces icaos, dans le cas idéal où l'API donne accès à l'historique des vols
        effectués par un icao dans les 30 derniers jours. default=None.

        to_csv (bool): si True, enregistre le dataset dans un fichier csv local après extraction des
        données.

        update (bool): si True, récupère le dataset, mis à jour via l'API OpenSky.
        si "False", récupère le dataset d'un fichier csv enregistré localement (enregistré dans Data
        si le paramètre "to_csv" est "True" lors d'une instanciation de cette classe)

        from_icao (bool): si True, les données sont extraites via la fonction de l'API OpenSKy permettant
        d'avoir l'historique des vols d'un icao donnée sur les 30 derniers jours. Par défault, la fonction
        est inaccessible donc les données sont récupérées avec une autre fonction qui donne directement tous
        les vols enregistrés par OpenSky sur les deux dernières heures.
        """
    def __init__(self, icaos=None, to_csv=True, update=True, from_icao=False):
        self.api = OpenSkyApi()
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
        # Si update=False, dataset récupéré localement (comme expliqué dans la classe AircraftsExtractor)
        else:
            self.df = pd.read_csv('Data/flights.csv')
        if to_csv:
            self.to_csv()
        self.icaos = self.df['icao'].unique().tolist()

    def get_data(self, icaos=None):
        """
        Extrait et construit le dataset "flights" (extract), contenant la liste des vols enregistrés par
        OpenSky ces 2 dernierès heures ou 30 derniers jours (fonctionnalité limitée par l'API)

        Paramètres:
        icaos (list): liste contenant les icaos desquels il faut rechercher l'historique des vols sur 30 jours,
        dans le cas idéal. 

        Retourne:
        Dataset "flights".
        """
        df = pd.DataFrame(columns=['icao','totaldist','totaltime'])
        if icaos == None: # Récupération des vols enregistrés par OpenSky dans les 2 dernières heures
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
        else: # Récupération des vols enregistrés par OpenSky dans les 30 derniers jours pour chaque icao 
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
        """
        Calcule la distance parcourue par l'avion qui a effectué le vol "flight", ainsi que le temps de vol

        Paramètres:
        flight: vol dont on veut extraire les caractéristiques intéressantes (contient par expl. les coordonnées
        des aéroports de départ et d'arrivée, et les horaires de départ et d'arrivée)

        Retourne:
        tuple: (Distance horizontale parcourue par l'avion, temps de vol depuis départ)
        """
        hor_dist_dep = flight.estDepartureAirportHorizDistance
        dep_time = flight.firstSeen
        arv_time = flight.lastSeen
        return hor_dist_dep, arv_time - dep_time
    
    def _are_airports_valid(self, flight):
        """
        Vérifie qu'un vol est "valide" (i.e. que ses aéroports de départ et d'arrivée sont valides, donc != None)

        Paramètres:
        flight: vol à vérifier

        Retourne:
        bool 
        """
        dep_airport = flight.estDepartureAirport
        if dep_airport is None:
            return False
        return True
    
    def transform(self, icaos, aircrafts):
        """
        Transformation finale du dataset pour que son format soit celui exigé par l'application, pour loading 
        en SQL. 
        En particulier, ne garde que les icaos qui sont présents dans le dataset "aircrafts" et ajoute une colonne
        contenant les émissions totales de CO2 des avions (icaos) du dataset.
        Paramètres:
        icaos (list): liste des icaos à garder dans le dataframe "aircrafts". Ces icaos sont censés être ceux
        du dataframe "flights".
        """
        self.df = self.df[self.df['icao'].isin(icaos)]
        self.icaos = self.df['icao'].unique().tolist()
        merged_df = self.df.merge(aircrafts[['icao24', 'CO2perkm']], left_on='icao', right_on='icao24')
        merged_df['kgCO2'] = (merged_df['totaldist'] / 1000 + 95) * merged_df['CO2perkm']
        self.df = merged_df.drop(columns=['icao24', 'CO2perkm'])

    def to_csv(self):
        """
        Enregistre le dataframe dans un csv.

        Paramètres:
        path (str): chemin d'enregistrement.
        """
        self.df.to_csv('Data/flights.csv', index=False)

    def to_database(self, db_url):
        """
        Upload le dataframe "flights" dans la base de données PostgreSQL spcifiée.

        Paramètres:
        db_url (str): URL de la base de données où le dataset sera stocké.
        """
        table_name = 'flights'
        engine = create_engine(db_url)
        with engine.connect() as connection:
            try:
                self.df.to_sql(table_name, con=connection, if_exists='replace', index=False)
                print(f"Data loaded successfully into {table_name}")
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                connection.close()