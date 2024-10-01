from opensky_api import OpenSkyApi
from datetime import datetime

api = OpenSkyApi()

start_str = "2024-09-15 12:00:00"

start_obj = datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S')

start_timestamp = int(start_obj.timestamp())
end_timestamp = int(datetime.now().timestamp())

data = api.get_flights_by_aircraft("3c675a", start_timestamp, end_timestamp)
for flight in data:
    print(flight)