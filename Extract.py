import pandas as pd

# Charger les données OpenFlights
routes_df = pd.read_csv('./Data_openflights/routes.dat', header=None)
airports_df = pd.read_csv('./Data_openflights/airports.dat', header=None)
