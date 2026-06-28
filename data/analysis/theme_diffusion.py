import pandas as pd

df = pd.read_csv(
    "data/analysis/idy_theme_corpus.csv"
)

df["year"] = (
    df["upload_date"]
      .astype(str)
      .str[:4]
)

text = (
    df["title"]
      .fillna("")
      .str.lower()
)

themes = {

    "self_and_society":
        "self and society",

    "one_earth":
        "one earth",

    "one_health":
        "one health",

    "healthy_ageing":
        "healthy ageing",

    "healthy_aging":
        "healthy aging"

}

rows = []

for year in sorted(df["year"].unique()):

    subset = df[
        df["year"] == year
    ]

    titles = (
        subset["title"]
          .fillna("")
          .str.lower()
    )

    row = {
        "year": year
    }

    for theme, phrase in themes.items():

        row[theme] = (
            titles.str.contains(
                phrase,
                regex=False
            )
            .sum()
        )

    rows.append(row)

out = pd.DataFrame(rows)

out.to_csv(
    "data/analysis/theme_diffusion.csv",
    index=False
)

print(out)
