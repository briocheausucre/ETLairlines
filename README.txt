SDD project on ETL a pipeline

scripty.py is the main script. for now, it extracts and transforms the data, need to compute the functions for loading. Leverages the two following files:

extract_aircrafts.py defines a class that extracts the aicrafts data, containing ICAOs and the corresponding airline for each aircraft. The dataset is either stored in a csv or stored as an attribute of the class, before being loaded to a SQL database.

extract_flights.py defines a class that extracts all the flights (if available) corresponding to each ICAO. Could extract data for the last 30 days with the required authorizations, but is now available only for the flights from 2 hours ago at most. The class transforms the data by calculating for each ICAO the distance flown and time fown. Next step is to evaluate the total CO2 emitted per ICAO in the given timeframe. A new dataset is made with these three variables (distance flown, time flown, CO2 emitted). The dataset is either stored in a csv or stored as an attribute of the class, before being loaded to a SQL database.
