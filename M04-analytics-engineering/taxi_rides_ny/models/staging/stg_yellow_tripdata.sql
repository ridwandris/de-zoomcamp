{{ config(materialized='view') }}

SELECT
    -- identifiers
    CAST(VendorID AS INT64) AS vendor_id,
    CAST(RatecodeID AS INT64) AS ratecode_id,
    CAST(PULocationID AS INT64) AS pickup_location_id,
    CAST(DOLocationID AS INT64) AS dropoff_location_id,

    -- timestamps
    CAST(tpep_pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(tpep_dropoff_datetime AS TIMESTAMP) AS dropoff_datetime,

    -- trip info
    store_and_fwd_flag,
    CAST(passenger_count AS INT64) AS passenger_count,
    CAST(trip_distance AS NUMERIC) AS trip_distance,

    -- payment info
    CAST(fare_amount AS NUMERIC) AS fare_amount,
    CAST(extra AS NUMERIC) AS extra,
    CAST(mta_tax AS NUMERIC) AS mta_tax,
    CAST(tip_amount AS NUMERIC) AS tip_amount,
    CAST(tolls_amount AS NUMERIC) AS tolls_amount,
    CAST(improvement_surcharge AS NUMERIC) AS improvement_surcharge,
    CAST(total_amount AS NUMERIC) AS total_amount,
    CAST(payment_type AS INT64) AS payment_type

FROM {{ source('staging', 'yellow_tripdata_non_partitioned') }}
WHERE VendorID IS NOT NULL