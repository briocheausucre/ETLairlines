SDD project on ETL a pipeline.

- `airlife.py` is a script to show and play with the little graphical interface we made. It has to be launched after `ETL.py`.

- `ETL.py` is the main script, that has to be launched first. Extracts, transforms and loads the data. Leverages the two following files:

- `extract_aircrafts.py` defines a class that extracts the aicrafts data, containing ICAOs and the corresponding airline and CO2 consumption per km (among other features) for each aircraft. The dataset is either stored in a csv or stored as an attribute of the class, before being loaded to a SQL database.

- `extract_flights.py` defines a class that extracts all the flights (if available) corresponding to each ICAO. Could extract data for the last 30 days with the required authorizations, but is now available only for the flights from 2 hours ago at most. The class transforms the data by calculating for each ICAO the distance flown and time fown. Next step is to evaluate the total CO2 emitted per ICAO in the given timeframe. A new dataset is made with these three variables (distance flown, time flown, CO2 emitted). The dataset is either stored in a csv or stored as an attribute of the class, before being loaded to a SQL database.

The created functions in both classes enable either downloading the data from the API (time consumming if the data is from the last 30 days, immediate for the last 2 hours) for updating the datasets, either directly load the data from the CSVs (but this data won't be up-to-date). For downloading from the API (thus updating the data), set `update=True` in the `ETL.py` file.

- To be able to import the API (from opensky_api import OpenSkyApi), one must :
    - clone the following repository : git@github.com:openskynetwork/opensky-api.git (if needed, see https://github.com/openskynetwork/opensky-api)
    - then activate the right Python environment using the bash
    - finally enter "pip install -e <path/to/the/repository>/python" in the bash

- To be able to re-create our tables, one has to create an empty database, and then adapt the db_url variable in the code `ETL.py` and in the code `airlife.py`:
    - Create a local database in a local server (we used Postgres.app to host a local PostgreSQL 17 server, in which we created  a database named "airlife")
    - At line 13 in `ETL.py` and line 7 in `airlife.py`, there is a variable db_url, set to 'postgresql://<username>:<password>@localhost:5432/<database_name>'. One has to replace <username> by its PostgreSQL username, <password> by its PostgreSQL password and <database_name> by the name of the local database. One has also to check if the port of the local server is correctly set-up (here, it's 5432).