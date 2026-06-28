import pandas as pd

df = pd.read_csv(
    "data/analysis/canonical_transcripts_clustered.csv"
)

for c in sorted(df["cluster"].unique()):

    print("\n" + "="*80)
    print("CLUSTER", c)
    print("="*80)

    sample = (
        df[df["cluster"] == c]
        .sample(10, random_state=42)
    )

    cols = [x for x in df.columns if x in [
        "video_id",
        "title",
        "channel",
        "year",
        "cluster"
    ]]

    print(sample[cols].to_string(index=False))
