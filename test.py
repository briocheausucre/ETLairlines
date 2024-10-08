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

result = df2[df2['icao24'].isin(df1['icao'])]['model']
print(result)

if 1 == 2:
    df2['CO2perkm'] = df2['model'].apply(lambda x: 
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
    

df2.to_csv('Data/aircrafts.csv', index=False)

#for index, row in df2.iterrows():
#    model_type = row['model']
#    if not isinstance(model_type, str):
#        print(f"Ligne {index}: Type de 'model' = {model_type}")

