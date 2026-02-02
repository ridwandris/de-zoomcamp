# Module 2 Homework - Solutions

## Answers

### Question 1
**Question:** Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?

**Answer:** 128.3 MiB

**Verification:** 
```bash
ls -lh yellow_tripdata_2020-12.csv
# Output: -rw-rw-r-- 1 ridwan ridwan 129M Jul 14  2022 yellow_tripdata_2020-12.csv
```

---

### Question 2
**Question:** What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

**Answer:** `green_tripdata_2020-04.csv`

**Explanation:** The template `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` renders with the provided inputs:
- `{{inputs.taxi}}` → `green`
- `{{inputs.year}}` → `2020`
- `{{inputs.month}}` → `04`

Result: `green_tripdata_2020-04.csv`

---

### Question 3
**Question:** How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?

**Answer:** 24,648,499

**Breakdown by month:**
- January 2020: 6,405,008
- February 2020: 6,299,354
- March 2020: 3,007,292
- April 2020: 237,993
- May 2020: 348,371
- June 2020: 549,760
- July 2020: 800,412
- August 2020: 1,007,284
- September 2020: 1,341,012
- October 2020: 1,681,131
- November 2020: 1,508,985
- December 2020: 1,461,897

**Total:** 24,648,499 rows

---

### Question 4
**Question:** How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?

**Answer:** 1,734,051

**Breakdown by month:**
- January 2020: 447,770
- February 2020: 398,632
- March 2020: 223,406
- April 2020: 35,612
- May 2020: 57,360
- June 2020: 63,109
- July 2020: 72,257
- August 2020: 81,063
- September 2020: 87,987
- October 2020: 95,120
- November 2020: 88,605
- December 2020: 83,130

**Total:** 1,734,051 rows

---

### Question 5
**Question:** How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?

**Answer:** 1,925,152

**Verification:**
```bash
# Downloaded and counted rows from yellow_tripdata_2021-03.csv.gz
# Result: 1,925,152 rows
```

---

### Question 6
**Question:** How would you configure the timezone to New York in a Schedule trigger?

**Answer:** Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration

**Explanation:** In Kestra (and most scheduling systems), timezones should be configured using IANA timezone database format (e.g., `America/New_York`), not abbreviations like `EST` or UTC offsets like `UTC-5`. This is because:
- EST doesn't account for Daylight Saving Time
- UTC offsets can vary with DST
- IANA timezone format (America/New_York) automatically handles DST transitions

**Example configuration:**
```yaml
triggers:
  - id: schedule
    type: io.kestra.core.models.triggers.types.Schedule
    cron: "0 9 * * *"
    timezone: America/New_York
```
