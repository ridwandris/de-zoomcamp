DROP TABLE IF EXISTS cleaned_statistics;

CREATE TABLE cleaned_statistics AS
SELECT 
    statistics_label AS category,
    time_label AS period,
    "1_variable_label" AS region_or_group,
    -- Handle both empty strings AND single dots as NULL
    CAST(
        NULLIF(NULLIF(value, ''), '.') 
        AS NUMERIC
    ) AS measure_value,
    value_unit AS unit
FROM my_raw_table
-- Only keep rows where the value is actually a number (not a dot or empty)
WHERE value IS NOT NULL 
  AND value != '' 
  AND value != '.';
