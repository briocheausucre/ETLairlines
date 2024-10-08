import pandas as pd

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
        else:
            aircrafts = pd.read_csv('Data/aircrafts.csv')
        return aircrafts
    
    def transform(self, icaos):
        df = self.df[self.df['icao24'].isin(icaos)]
        df = df[['icao24', 'model', 'operator', 'operatorcallsign', 'CO2perkm']]
        df['operator'] = df.apply(
        lambda row: row['operatorcallsign'] if row['operatorcallsign'] is not None 
        else row['operator'], axis=1
        )
        self.df = df.drop(columns=['operatorcallsign'])
        self.icaos = icaos

    def to_csv(self, path='Data/aircrafts.csv'):
        self.df.to_csv(path, index=False)

    def to_database(self):
        '''
        Uploads the aircrafts dataset to the SQL online database
        '''
        pass