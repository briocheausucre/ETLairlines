import pandas as pd

aircrafts = pd.read_csv('Data/aircrafts.csv',index_col=0)

print(aircrafts.head())