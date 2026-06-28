import pandas as pd

df = pd.read_csv(
    "data/analysis/cluster_interpretation.csv"
)

table = pd.crosstab(
    df["cluster"],
    df["channel"]
)

for c in sorted(df["cluster"].unique()):

    print("\nCLUSTER", c)

    print(
        table.loc[c]
        .sort_values(ascending=False)
        .head(15)
    )
