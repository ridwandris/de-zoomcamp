import pandas as pd
from sqlalchemy import create_engine

url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
print(f"Downloading data from {url}...")

datatypes = {
    'LocationID': 'int32',
    'Borough': 'string',
    'Zone': 'string',
    'service_zone': 'string'
}

print("Data downloaded successfully. Here are the first few rows:")

df = pd.read_csv(url, dtype=datatypes)

engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')

print("Pushing data to PostgreSQL...")

df.to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace', index=False)

print("Success!")