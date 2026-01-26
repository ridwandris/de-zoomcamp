import pandas as pd
import pyarrow.parquet as pq

# Load the data
print("Loading data...")
green_taxi = pd.read_parquet('green_tripdata_2025-11.parquet')
zones = pd.read_csv('taxi_zone_lookup.csv')

print(f"\nGreen taxi data shape: {green_taxi.shape}")
print(f"Zones data shape: {zones.shape}")

print("\nGreen taxi columns:")
print(green_taxi.columns.tolist())

print("\nZones columns:")
print(zones.columns.tolist())

# Question 3: Count trips with distance <= 1 mile in November 2025
print("\n" + "="*60)
print("QUESTION 3: Trips with distance <= 1 mile")
print("="*60)

# Filter for November 2025 trips
green_taxi['lpep_pickup_datetime'] = pd.to_datetime(green_taxi['lpep_pickup_datetime'])
nov_trips = green_taxi[
    (green_taxi['lpep_pickup_datetime'] >= '2025-11-01') & 
    (green_taxi['lpep_pickup_datetime'] < '2025-12-01')
]

# Count trips with distance <= 1 mile
short_trips = nov_trips[nov_trips['trip_distance'] <= 1.0]
print(f"Number of trips with distance <= 1 mile: {len(short_trips)}")

# Question 4: Day with longest trip distance (excluding errors > 100 miles)
print("\n" + "="*60)
print("QUESTION 4: Day with longest trip distance")
print("="*60)

# Filter trips with distance < 100 miles
valid_trips = nov_trips[nov_trips['trip_distance'] < 100]

# Find the trip with the max distance
max_trip = valid_trips.loc[valid_trips['trip_distance'].idxmax()]
print(f"Longest trip distance: {max_trip['trip_distance']} miles")
print(f"Pickup datetime: {max_trip['lpep_pickup_datetime']}")
print(f"Pickup day: {max_trip['lpep_pickup_datetime'].date()}")

# Question 5: Pickup zone with largest total_amount on Nov 18, 2025
print("\n" + "="*60)
print("QUESTION 5: Pickup zone with largest total_amount on Nov 18")
print("="*60)

# Filter for Nov 18, 2025
nov_18_trips = nov_trips[nov_trips['lpep_pickup_datetime'].dt.date == pd.to_datetime('2025-11-18').date()]

# Group by pickup location ID and sum total_amount
pickup_totals = nov_18_trips.groupby('PULocationID')['total_amount'].sum().reset_index()
pickup_totals = pickup_totals.sort_values('total_amount', ascending=False)

# Merge with zones to get zone names
pickup_totals = pickup_totals.merge(zones, left_on='PULocationID', right_on='LocationID', how='left')

print("\nTop 5 pickup zones by total_amount on Nov 18:")
print(pickup_totals[['Zone', 'total_amount']].head())

# Question 6: Dropoff zone with largest tip from East Harlem North in November 2025
print("\n" + "="*60)
print("QUESTION 6: Dropoff zone with largest tip from East Harlem North")
print("="*60)

# Find LocationID for East Harlem North
east_harlem_north = zones[zones['Zone'] == 'East Harlem North']
print(f"\nEast Harlem North LocationID: {east_harlem_north['LocationID'].values}")

if len(east_harlem_north) > 0:
    ehn_id = east_harlem_north['LocationID'].values[0]
    
    # Filter trips picked up in East Harlem North in November 2025
    ehn_trips = nov_trips[nov_trips['PULocationID'] == ehn_id]
    
    print(f"Number of trips from East Harlem North in Nov 2025: {len(ehn_trips)}")
    
    # Group by dropoff location and find max tip
    dropoff_tips = ehn_trips.groupby('DOLocationID')['tip_amount'].max().reset_index()
    dropoff_tips = dropoff_tips.sort_values('tip_amount', ascending=False)
    
    # Merge with zones to get zone names
    dropoff_tips = dropoff_tips.merge(zones, left_on='DOLocationID', right_on='LocationID', how='left')
    
    print("\nTop 5 dropoff zones by largest tip:")
    print(dropoff_tips[['Zone', 'tip_amount']].head())
else:
    print("East Harlem North not found in zones data")

print("\n" + "="*60)
print("Analysis complete!")
print("="*60)
