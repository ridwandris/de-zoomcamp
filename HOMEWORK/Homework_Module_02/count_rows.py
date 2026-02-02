#!/usr/bin/env python3
"""Count rows in NYC taxi data for homework answers."""

import pandas as pd
import requests
import gzip
import io

def count_rows_for_year(taxi_type, year, months):
    """Count total rows for a specific taxi type and year."""
    total_rows = 0
    base_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/"
    
    for month in months:
        month_str = str(month).zfill(2)
        filename = f"{taxi_type}_tripdata_{year}-{month_str}.csv.gz"
        url = base_url + filename
        
        print(f"Processing {filename}...")
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                # Read compressed data using pandas
                df = pd.read_csv(io.BytesIO(response.content), compression='gzip')
                rows = len(df)
                total_rows += rows
                print(f"  Rows: {rows:,}")
            else:
                print(f"  Failed to download (Status: {response.status_code})")
        except Exception as e:
            print(f"  Error: {e}")
    
    return total_rows

def count_rows_single_file(taxi_type, year, month):
    """Count rows in a single file."""
    base_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{taxi_type}/"
    month_str = str(month).zfill(2)
    filename = f"{taxi_type}_tripdata_{year}-{month_str}.csv.gz"
    url = base_url + filename
    
    print(f"Processing {filename}...")
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            df = pd.read_csv(io.BytesIO(response.content), compression='gzip')
            rows = len(df)
            print(f"  Rows: {rows:,}")
            return rows
        else:
            print(f"  Failed to download (Status: {response.status_code})")
            return 0
    except Exception as e:
        print(f"  Error: {e}")
        return 0

if __name__ == "__main__":
    # Question 3: Yellow taxi for all of 2020
    print("\n=== Question 3: Yellow Taxi 2020 ===")
    yellow_2020_total = count_rows_for_year("yellow", 2020, range(1, 13))
    print(f"\nTotal Yellow Taxi rows for 2020: {yellow_2020_total:,}\n")
    
    # Question 4: Green taxi for all of 2020
    print("\n=== Question 4: Green Taxi 2020 ===")
    green_2020_total = count_rows_for_year("green", 2020, range(1, 13))
    print(f"\nTotal Green Taxi rows for 2020: {green_2020_total:,}\n")
    
    # Question 5: Yellow taxi for March 2021
    print("\n=== Question 5: Yellow Taxi March 2021 ===")
    yellow_2021_03 = count_rows_single_file("yellow", 2021, 3)
    print(f"\nTotal Yellow Taxi rows for March 2021: {yellow_2021_03:,}\n")
