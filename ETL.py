from extract_aircrafts import AircraftsExtractor
from extract_flights import FlightsExtractor


if __name__ == "__main__":

    # Extraction des datasets (aéronefs / vols correspondants) et premières transformations
    aircrafts_extractor = AircraftsExtractor(update=True)
    flights_extractor = FlightsExtractor(aircrafts_extractor.icaos, update=True)

    # Transformation des données (nettoyage des données, ajout colonne emissions CO2)
    flights_extractor.transform(aircrafts_extractor.icaos, aircrafts_extractor.df)
    aircrafts_extractor.transform(flights_extractor.icaos)

    # Upload des datasets sur un serveur PostgreSQL
    db_url = 'postgresql://astel:Lexanahoj1972!@localhost:5432/airlife'
    aircrafts_extractor.to_database(db_url)
    flights_extractor.to_database(db_url)