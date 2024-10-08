import pandas as pd

class AicraftsExtractor():
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

    def to_csv(self):
        self.df.to_csv('Data/aircrafts.csv', index=False)

    def to_database(self):
        '''
        Uploads the aircrafts dataset to the SQL online database
        '''
        pass