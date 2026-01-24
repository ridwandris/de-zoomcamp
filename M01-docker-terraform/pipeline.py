import sys
import pandas as pd


print("arguments", sys.argv)

if len(sys.argv) < 2:
    print("Error: Please provide a day number")
    print("Usage: python pipeline.py <day>")
    sys.exit(1)

day = int(sys.argv[1])
print(f"Running pipeline for day {day}")

df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")