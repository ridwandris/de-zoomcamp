##  Module 3 Homework Solution

## Question 1:
What is count of records for the 2024 Yellow Taxi Data?
I used 
```bash
SELECT COUNT(*)
FROM `dtc-de-course-488907.hw3_dataset.yellow_tripdata_non_partitioned`;
```
- 20,332,093


## Question 2:
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?
```bash
SELECT COUNT(DISTINCT PULocationID)
FROM `dtc-de-course-488907.hw3_dataset.external_yellow_tripdata`;

SELECT COUNT(DISTINCT PULocationID)
FROM `dtc-de-course-488907.hw3_dataset.yellow_tripdata_non_partitioned`
```
- 0 MB for the External Table and 155.12 MB for the Materialized Table

## Question 3:
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
```bash
SELECT PULocationID, --DOLocationID
FROM `dtc-de-course-488907.hw3_dataset.yellow_tripdata_non_partitioned`;
```
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires 
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

## Question 4:
How many records have a fare_amount of 0?
```bash
SELECT COUNT(*)
FROM `dtc-de-course-488907.hw3_dataset.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;
```
- 8,333

## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID


## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime
2024-03-01 and 2024-03-15 (inclusive)</br>
```bash
SELECT COUNT(*)
FROM `dtc-de-course-488907.hw3_dataset.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;
```
Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table


## Question 7: 
Where is the data stored in the External Table you created?

- GCP Bucket

## Question 8:
It is best practice in Big Query to always cluster your data:
- False


## (Bonus: Not worth points) Question 9:
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
- 0 MB, this is beacuse the Number of records is in metadata form in the non-partitioned/materialed table (BigQuery keeps a metadata file attached to the table), therefore it does not need to go through, read and process them.

## Submitting the solutions

Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw3

## Solution

Solution: https://www.youtube.com/watch?v=wpLmImIUlPg
