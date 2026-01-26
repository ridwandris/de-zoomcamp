# Module 1 Homework Answers

## Question 1. Understanding Docker images
**What's the version of `pip` in the python:3.13 image?**

**Answer: 25.3**

Command used:
```bash
docker run --rm -it --entrypoint bash python:3.13 -c "pip --version"
```

Output:
```
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

---

## Question 2. Understanding Docker networking and docker-compose
**What is the `hostname` and `port` that pgadmin should use to connect to the postgres database?**

**Answer: db:5432**

Explanation:
In docker-compose, containers on the same network can communicate using the service name as the hostname. The service is named "db" and PostgreSQL runs on its internal port 5432 (not the host-mapped port 5433).

---

## Question 3. Counting short trips
**For the trips in November 2025, how many trips had a `trip_distance` of less than or equal to 1 mile?**

**Answer: 8,007**

SQL Query (equivalent logic):
```sql
SELECT COUNT(*)
FROM green_tripdata_2025_11
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1.0;
```

---

## Question 4. Longest trip for each day
**Which was the pick up day with the longest trip distance?**

**Answer: 2025-11-14**

The longest trip (88.03 miles) occurred on 2025-11-14 at 15:36:27.

SQL Query (equivalent logic):
```sql
SELECT DATE(lpep_pickup_datetime) as pickup_day, MAX(trip_distance) as max_distance
FROM green_tripdata_2025_11
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

---

## Question 5. Biggest pickup zone
**Which was the pickup zone with the largest `total_amount` on November 18th, 2025?**

**Answer: East Harlem North**

Total amount: $9,281.92

SQL Query (equivalent logic):
```sql
SELECT z.Zone, SUM(g.total_amount) as total
FROM green_tripdata_2025_11 g
JOIN taxi_zone_lookup z ON g.PULocationID = z.LocationID
WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z.Zone
ORDER BY total DESC
LIMIT 1;
```

Top 5 results:
1. East Harlem North - $9,281.92
2. East Harlem South - $6,696.13
3. Central Park - $2,378.79
4. Washington Heights South - $2,139.05
5. Morningside Heights - $2,100.59

---

## Question 6. Largest tip
**For passengers picked up in East Harlem North in November 2025, which was the drop off zone that had the largest tip?**

**Answer: Yorkville West**

Largest tip: $81.89

SQL Query (equivalent logic):
```sql
SELECT dz.Zone, MAX(g.tip_amount) as max_tip
FROM green_tripdata_2025_11 g
JOIN taxi_zone_lookup pz ON g.PULocationID = pz.LocationID
JOIN taxi_zone_lookup dz ON g.DOLocationID = dz.LocationID
WHERE pz.Zone = 'East Harlem North'
  AND DATE(g.lpep_pickup_datetime) >= '2025-11-01'
  AND DATE(g.lpep_pickup_datetime) < '2025-12-01'
GROUP BY dz.Zone
ORDER BY max_tip DESC
LIMIT 1;
```

Top 5 results:
1. Yorkville West - $81.89
2. LaGuardia Airport - $50.00
3. East Harlem North - $45.00
4. Long Island City/Queens Plaza - $34.25

---

## Question 7. Terraform Workflow
**Which of the following sequences describes the workflow for:**
1. Downloading the provider plugins and setting up backend
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform

**Answer: terraform init, terraform apply -auto-approve, terraform destroy**

Explanation:
- `terraform init` - Initializes the working directory, downloads provider plugins, and sets up the backend
- `terraform apply -auto-approve` - Creates an execution plan and automatically applies it without asking for confirmation
- `terraform destroy` - Destroys all resources managed by the Terraform configuration

---

## Data Files
- Green taxi trips data: `green_tripdata_2025-11.parquet` (46,912 records)
- Zone lookup data: `taxi_zone_lookup.csv` (265 zones)

## Analysis Script
The answers were generated using Python with pandas and pyarrow libraries. See `analyze_data.py` for the complete analysis code.
