from sqlalchemy import create_engine, text

# Connection to Docker Postgres
engine = create_engine('postgresql://user:password@localhost:5432/main_db')

# Path to your SQL file
sql_file_path = '../sql/transform_data.sql'

try:
    with engine.connect() as conn:
        print("Reading SQL transformation script...")
        with open(sql_file_path, 'r') as file:
            query = file.read()
        
        print("Executing transformation...")
        conn.execute(text(query))
        conn.commit()
        print("Success! Cleaned table created.")

except Exception as e:
    print(f"Error: {e}")
