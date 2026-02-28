import pandas as pd

# Import the create_engine function from SQLAlchemy to establish a connection to the PostgreSQL database
from sqlalchemy import create_engine

# library to show progress of the data insertion
from tqdm.auto import tqdm
import click



# Define the data types for each column to optimize memory usage
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--pg-user', default='root', show_default=True, help='PostgreSQL user name.')
@click.option('--pg-password', default='root', show_default=True, help='PostgreSQL user password.')
@click.option('--pg-host', default='localhost', show_default=True, help='PostgreSQL host name.')
@click.option('--pg-port', default=5432, show_default=True, type=int, help='PostgreSQL port number.')
@click.option('--pg-db', default='ny_taxi', show_default=True, help='PostgreSQL database name.')
@click.option('--year', default=2021, show_default=True, type=int, help='Dataset year to ingest.')
@click.option('--month', default=1, show_default=True, type=int, help='Dataset month to ingest.')
@click.option('--target-table', default='yellow_taxi_data', show_default=True, help='Destination table name.')
@click.option('--chunksize', default=100000, show_default=True, type=int, help='Number of rows processed per chunk.')
def run(pg_user, pg_password, pg_host, pg_port, pg_db, year, month, target_table, chunksize):

    # Construct the URL for the CSV file based on the specified year and month
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    # Create the SQLAlchemy engine to connect to the PostgreSQL database
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')

    # Read the data in chunks and insert into the database
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first_chunk = True

    for df_chunk in tqdm(df_iter):
        if first_chunk:
            df_chunk.to_sql(
                name=target_table,
                con=engine, 
                if_exists='replace'
            )
            first_chunk = False

        else:
            df_chunk.to_sql( 
                name=target_table,
                con=engine, 
                if_exists='append'
                )

if __name__ == '__main__':
    run()