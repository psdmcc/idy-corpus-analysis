import pandas as pd

df = pd.read_csv(
    "data/analysis/canonical_transcripts_clustered.csv"
)

for c in sorted(df["cluster"].unique()):

    print("\n" + "="*60)
    print("CLUSTER", c)
    print("="*60)

    sample = (
        df[df["cluster"] == c]
        .sample(10, random_state=42)
    )

    for vid in sample["video_id"]:
        print(vid)
