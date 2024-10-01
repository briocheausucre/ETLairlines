import pandas as pd

# Charger les données OpenFlights
routes_df = pd.read_csv('./Data/routes.dat', header=None)
airports_df = pd.read_csv('./Data/airports.dat', header=None)
