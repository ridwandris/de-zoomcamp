import os
import urllib.request
from google.cloud import storage

# --- CONFIGURATION ---
# Change this to your actual GCP Bucket Name!
BUCKET_NAME = "kestra-demo-bucket-ridwan99" 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../keys/my-creds.json" # service account key

# What we need: Yellow (19-20), Green (19-20), FHV (19)
SERVICES = {
    'yellow': ['2019', '2020'],
    'green':  ['2019', '2020'],
    'fhv':    ['2019']
}

client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

for service, years in SERVICES.items():
    for year in years:
        for month in range(1, 13):
            file_name = f"{service}_tripdata_{year}-{month:02d}.csv.gz"
            url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{service}/{file_name}"
            
            print(f"Downloading {file_name}...")
            try:
                urllib.request.urlretrieve(url, file_name)
                
                print(f"Uploading {file_name} to GCS...")
                blob = bucket.blob(f"{service}/{file_name}")
                blob.upload_from_filename(file_name)
                
                os.remove(file_name) # Clean up local laptop space!
                print(f"✅ Success: {file_name}")
            except Exception as e:
                print(f"❌ Skipping {file_name} (Not found or error)")