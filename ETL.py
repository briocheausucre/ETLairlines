from extract_aircrafts import AircraftsExtractor
from extract_flights import FlightsExtractor


if __name__ == "__main__":

    aircrafts_extractor = AircraftsExtractor(update=False)
    flights_extractor = FlightsExtractor(aircrafts_extractor.icaos, update=False)

    flights_extractor.transform(aircrafts_extractor.icaos, aircrafts_extractor.df['CO2perkm'])
    aircrafts_extractor.transform(flights_extractor.icaos)

    db_url = 'postgresql://astel:Lexanahoj1972!@localhost:5432/airlife'
    aircrafts_extractor.to_database(db_url)
    flights_extractor.to_database(db_url)

    #print(flights_extractor.df)
    #print(aircrafts_extractor.df)



