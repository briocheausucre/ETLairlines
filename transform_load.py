import pandas as pd
from sqlalchemy import create_engine
import psycopg2

df = pd.read_csv("pandas_examples/RealMedicalData.csv", sep=';')

def load_to_postgresql(df, table_name, db_url):
    engine = create_engine(db_url)
    
    with engine.connect() as connection:
        try:
            # Load data to the specified table
            df.to_sql(table_name, con=connection, if_exists='append', index=False)
            print(f"Data loaded successfully into {table_name}")
        except Exception as e:
            print(f"Error loading data: {e}")
        finally:
            connection.close()

# PostgreSQL database URL
db_url = 'postgresql://astel:Lexanahoj1972!@localhost:5432/airlife'
load_to_postgresql(df, 'test_table', db_url)