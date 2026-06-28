import pandas as pd

df = pd.read_csv("dsi_rows.csv")

print("Rows:", len(df))
print("Columns:")
print(df.columns.tolist())
