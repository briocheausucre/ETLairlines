from extract_aircrafts import AicraftsExtractor
from extract_flights import FlightsExtractor


if __name__ == "__main__":

    aicrafts_extractor = AicraftsExtractor(update=False)
    flights_extractor = FlightsExtractor(aicrafts_extractor.icaos, update=True, from_icao=False)
    aicrafts_extractor.to_database()
    flights_extractor.to_database()


