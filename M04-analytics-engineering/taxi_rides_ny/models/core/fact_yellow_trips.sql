{{ config(materialized='table') }}

WITH trip_data AS (
    SELECT * FROM {{ ref('stg_yellow_tripdata') }}
),

zone_lookup AS (
    SELECT * FROM {{ ref('taxi_zone_lookup') }}
)

SELECT 
    trip_data.*, 
    pickup_zone.Borough AS pickup_borough, 
    pickup_zone.Zone AS pickup_zone, 
    dropoff_zone.Borough AS dropoff_borough, 
    dropoff_zone.Zone AS dropoff_zone  

FROM trip_data
INNER JOIN zone_lookup AS pickup_zone
    ON trip_data.pickup_location_id = pickup_zone.LocationID
INNER JOIN zone_lookup AS dropoff_zone
    ON trip_data.dropoff_location_id = dropoff_zone.LocationID