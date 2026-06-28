import pandas as pd

df = pd.read_csv(
    "data/analysis/cluster_interpretation.csv"
)

for c in sorted(df["cluster"].unique()):

    print("\n" + "="*100)
    print("CLUSTER", c)
    print("="*100)

    sample = (
        df[df["cluster"] == c]
        [["title", "channel"]]
        .sample(
            min(15, len(df[df["cluster"] == c])),
            random_state=42
        )
    )

    print(sample.to_string(index=False))
