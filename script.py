from extract_aircrafts import AircraftsExtractor
from extract_flights import FlightsExtractor


if __name__ == "__main__":

    aircrafts_extractor = AircraftsExtractor(update=False)
    flights_extractor = FlightsExtractor(aircrafts_extractor.icaos, update=False)

    flights_extractor.transform(aircrafts_extractor.icaos)
    aircrafts_extractor.transform(flights_extractor.icaos)

    aircrafts_extractor.to_database()
    flights_extractor.to_database()

    aircrafts_extractor.df.to_csv('Data/test.csv')
    print(flights_extractor.df.head())
    print(aircrafts_extractor.df.head())

