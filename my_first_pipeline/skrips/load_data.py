import pandas as pd
from sqlalchemy import create_engine

# 1. Setup the connection to your Docker Postgres
# Format: postgresql://user:password@localhost:5432/database_name
engine = create_engine('postgresql://user:password@localhost:5432/main_db')

# 2. Path to your file
file_path = '../rawdata/61262-0001_en_flat.csv'

try:
    # 3. Read the CSV
    print("Reading CSV file...")
    df = pd.read_csv(file_path, sep=';')

    # 4. Upload to Postgres
    print("Uploading to PostgreSQL...")
    df.to_sql('my_raw_table', engine, if_exists='replace', index=False)
    
    print("Success! Data loaded into 'my_raw_table'.")

except Exception as e:
    print(f"An error occurred: {e}")