import pandas as pd

df = pd.read_csv(
    "data/analysis/idy_theme_corpus.csv"
)

df["year"] = (
    df["upload_date"]
      .astype(str)
      .str[:4]
)

top_channels = (
    df["channel"]
    .value_counts()
    .head(25)
    .index
)

table = pd.crosstab(
    df["channel"],
    df["year"]
)

table = table.loc[
    table.index.intersection(
        top_channels
    )
]

table.to_csv(
    "data/analysis/actor_theme_matrix.csv"
)

print(table)
