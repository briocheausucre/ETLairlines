from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import requests
import pandas as pd


api = OpenSkyApi()
start_timestamp = int((datetime.now() - timedelta(hours=2)).timestamp())
end_timestamp = int(datetime.now().timestamp())
#flights = api.get_flights_from_interval(start_timestamp, end_timestamp)
#for flight in flights:
#    print(flight)


df1 = pd.read_csv('Data/flights.csv')

df2 = pd.read_csv('Data/aircrafts.csv')

result = df1[df1['icao'].isin(df2['icao24'])]
print(result)