import pandas as pd

df = pd.read_csv("dsi_rows.csv")

vc = df["channel"].value_counts()

channels = vc.reset_index()
channels.columns = ["channel", "count"]

channels.to_csv("unique_channels.csv", index=False)

print(df["channel"].nunique())
