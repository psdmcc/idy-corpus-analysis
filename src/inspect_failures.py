import pandas as pd

meta = pd.read_csv(
    "data/transcripts_recovered_pilot/pilot_metadata.csv"
)

failed = meta[
    meta["success"] == False
]

print(
    failed["error"]
    .value_counts()
)
