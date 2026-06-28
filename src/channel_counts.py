import pandas as pd

df = pd.read_csv("dsi_rows.csv")

counts = (
    df["channel"]
    .value_counts()
    .reset_index()
)

counts.columns = ["channel", "count"]

print(counts.to_string(index=False))

print("\n--- Top 50 coverage ---")

top50 = df["channel"].value_counts().head(50)

print("Number of channels:", len(top50))
print("Transcripts represented:", top50.sum())
print("Corpus size:", len(df))
print("Coverage:", round(100 * top50.sum() / len(df), 1), "%")

for n in [10, 25, 50, 100]:
    topn = df["channel"].value_counts().head(n)
    print(
        f"Top {n}: "
        f"{topn.sum()} transcripts "
        f"({100*topn.sum()/len(df):.1f}%)"
    )

vc = df["channel"].value_counts()

print((vc >= 3).sum())
print(vc[vc >= 3].sum())
