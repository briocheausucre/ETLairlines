import pandas as pd
from sqlalchemy import create_engine
import psycopg2

class AircraftsExtractor():
    """
        Classe pour extraire, transformer et load le dataset "aircrafts".

        Paramètres:

        to_csv (bool): si True, enregistre le dataset dans un fichier csv local après extraction des
        données.

        update (bool): si True, récupère le dataset, mis à jour via l'API OpenSky.
        si "False", récupère le dataset d'un fichier csv enregistré localement (enregistré dans Data
        si le paramètre "to_csv" est "True" lors d'une instanciation de cette classe)
        """
    def __init__(self, to_csv=True, update=False):
        self.df = self.get_data(update)
        self.icaos = self.df['icao24'].unique().tolist()
        if to_csv:
            self.to_csv()

    def get_data(self, update):
        """
        Récupère le dataset "aircrafts" (extract), contenant la liste de tous les aéronèfs en circulation.

        Paramètres:
        update (bool): si "True", récupère le dataset, mis à jour via l'API OpenSky.
        si "False", récupère le dataset d'un fichier csv enregistré localement (enregistré dans Data
        si le paramètre "to_csv" est "True" lors d'une instanciation de cette classe)

        Retourne:
        Dataset "aircrafts".
        """
        if update:
            aircrafts = pd.read_csv('https://opensky-network.org/datasets/metadata/aircraftDatabase.csv')
            aircrafts = aircrafts[aircrafts['manufacturername'].isin(['Airbus', 'Boeing'])]    
            aircrafts['CO2perkm'] = aircrafts['model'].apply(lambda x: 
                                                    (1.9 if '737' in x else 
                                                    3.5 if '747' in x else
                                                    3.5 if 'A330' in x else
                                                    4.0 if '777' in x else
                                                    2.2 if 'A320' in x else
                                                    3.0 if '787' in x else
                                                    1.7 if 'A319' in x else
                                                    2.1 if 'A321' in x else
                                                    2.6 if 'A350' in x else
                                                    3.8 if '767' in x else
                                                    3.2 if '757' in x else
                                                    3) if isinstance(x, str) else 3)
        else:
            aircrafts = pd.read_csv('Data/aircrafts.csv')
        return aircrafts
    
    def transform(self, icaos):
        """
        Transformation finale du dataset pour que son format soit celui exigé par l'application, pour loading 
        en SQL. 
        En particulier, ne garde que les colonnes utiles à l'application: icao, modèle de l'avion, compagnie 
        aérienne, consommation de CO2 moyenne par km.

        Paramètres:
        icaos (list): liste des icaos à garder dans le dataframe "aircrafts". Ces icaos sont censés être ceux
        du dataframe "flights".
        """

        df = self.df[self.df['icao24'].isin(icaos)].reset_index(drop=True)
        df = df[['icao24', 'model', 'operator', 'operatorcallsign', 'CO2perkm']]
        df['operator'] = df.apply(
        lambda row: row['operatorcallsign'] if row['operatorcallsign'] is not None 
        else row['operator'], axis=1
        )
        self.df = df.drop(columns=['operatorcallsign'])
        self.icaos = icaos

    def to_csv(self, path='Data/aircrafts.csv'):
        """
        Enregistre le dataframe dans un csv.

        Paramètres:
        path (str): chemin d'enregistrement.
        """
        self.df.to_csv(path, index=False)

    def to_database(self, db_url):
        """
        Upload le dataframe "aircrafts" dans la base de données PostgreSQL spcifiée.

        Paramètres:
        db_url (str): URL de la base de données où le dataset sera stocké.
        """
        table_name = 'aircrafts'
        engine = create_engine(db_url)
        with engine.connect() as connection:
            try:
                self.df.to_sql(table_name, con=connection, if_exists='replace', index=False)
                print(f"Data loaded successfully into {table_name}")
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                connection.close()