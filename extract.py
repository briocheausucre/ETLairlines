import pandas as pd

# Charger les données OpenFlights
routes_df = pd.read_csv('./Data/routes.dat', header=None)
airports_df = pd.read_csv('./Data/airports.dat', header=None)

import requests
from datetime import datetime, timedelta, timezone

# Informations de connexion (remplace par tes identifiants OpenSky)
username = 'Hippolyte'
password = 'dyqXex-tajwij-fuzpa7'

# Récupérer l'heure actuelle et définir un intervalle pour les données historiques
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=30)  # Limite à 2 jours
start_timestamp = int(start_time.timestamp())
end_timestamp = int(end_time.timestamp())

# URL de l'API OpenSky pour récupérer les données des vols
url = f"https://opensky-network.org/api/flights/aircraft?icao24=3c675a&begin={start_timestamp}&end={end_timestamp}"
print("URL de la requête :", url)  # Imprime l'URL pour débogage

# Effectuer la requête API
response = requests.get(url, auth=(username, password))

# Vérification de la réponse
if response.status_code == 200:
    flights_data = response.json()
    
    # Vérification des données reçues
    print("Données de vol récupérées :", flights_data)  # Imprime les données pour débogage
    
    # Filtrer les données pour un avion spécifique, par exemple, avec un identifiant unique
    aircraft_icao24 = '4CA97B'  # Remplace par l'ICAO24 de l'avion que tu veux suivre
    aircraft_flights = [flight for flight in flights_data if flight['icao24'] == aircraft_icao24]

    if aircraft_flights:
        for flight in aircraft_flights:
            print(f"Vol : {flight['callsign']}, Distance : {flight['distance']}, Heure de départ : {flight['departureTime']}")
    else:
        print("Aucun vol trouvé pour cet avion.")
else:
    print(f"Erreur lors de la requête API : {response.status_code}")
    print("Message d'erreur :", response.text)  # Imprime le message d'erreur pour débogag