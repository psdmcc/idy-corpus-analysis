import pandas as pd

df = pd.read_csv(
    "data/analysis/canonical_transcripts_clustered_meta.csv"
)

for cluster in sorted(df["cluster"].unique()):

    print("\n" + "=" * 80)
    print("CLUSTER", cluster)
    print("=" * 80)

    sample = (
        df[df["cluster"] == cluster]
        .sample(
            min(5, len(df[df["cluster"] == cluster])),
            random_state=42
        )
    )

    print(
        sample[
            [
                "title",
                "channel",
                "year",
                "video_id"
            ]
        ].to_string(index=False)
    )
