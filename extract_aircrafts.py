import pandas as pd
from sqlalchemy import create_engine
import psycopg2

class AircraftsExtractor():
    def __init__(self, to_csv=True, update=False):
        self.df = self.get_data(update)
        self.icaos = self.df['icao24'].unique().tolist()
        if to_csv:
            self.to_csv()

    def get_data(self, update):
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
        df = self.df[self.df['icao24'].isin(icaos)].reset_index(drop=True)
        df = df[['icao24', 'model', 'operator', 'operatorcallsign', 'CO2perkm']]
        df['operator'] = df.apply(
        lambda row: row['operatorcallsign'] if row['operatorcallsign'] is not None 
        else row['operator'], axis=1
        )
        self.df = df.drop(columns=['operatorcallsign'])
        self.icaos = icaos

    def to_csv(self, path='Data/aircrafts.csv'):
        self.df.to_csv(path, index=False)

    def to_database(self, db_url):
        '''
        Uploads the aircrafts dataset to the SQL online database
        '''
        table_name = 'aircrafts'
        engine = create_engine(db_url)
        with engine.connect() as connection:
            try:
                self.df.to_sql(table_name, con=connection, if_exists='append', index=False)
                print(f"Data loaded successfully into {table_name}")
            except Exception as e:
                print(f"Error loading data: {e}")
            finally:
                connection.close()