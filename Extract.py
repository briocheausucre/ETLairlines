from opensky_api import OpenSkyApi
from datetime import datetime
import pandas as pd

api = OpenSkyApi()

start_str = "2024-09-15 12:00:00"
end_str = "2024-01-29 20:00:00"

start_obj = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')
end_obj = datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S')

start_timestamp = int(start_obj.timestamp())
end_timestamp = int(datetime.now().timestamp())

#data = api.get_flights_by_aircraft("3c675a", start_timestamp, end_timestamp)
#for flight in data:
#    print(flight)

aircrafts = pd.read_csv('Data/aircrafts.csv',index_col=0)

print(aircrafts.head())