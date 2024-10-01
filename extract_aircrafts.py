import pandas as pd

aircrafts = pd.read_csv('https://opensky-network.org/datasets/metadata/aircraftDatabase.csv')
aircrafts = aircrafts[aircrafts['manufacturername'].isin(['Airbus', 'Boeing'])]
print(aircrafts.head())


### OR ###

aircrafts = pd.read_csv('Data/aircrafts.csv', index_col=0)
print(aircrafts.head())