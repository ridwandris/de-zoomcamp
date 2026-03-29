{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
        -- identifiers
        cast(dispatching_base_num as string) as dispatching_base_num,
        cast(PUlocationID as integer) as pickup_location_id,
        cast(DOlocationID as integer) as dropoff_location_id,

        -- timestamps
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropOff_datetime as timestamp) as dropoff_datetime,

        -- base number
        cast(Affiliated_base_number as string) as affiliated_base_number,
        
        -- shared ride flag
        cast(SR_Flag as string) as sr_flag

    from source
    -- Homework Requirement: Filter out records with null dispatching_base_num
    where dispatching_base_num is not null
)

select * from renamed