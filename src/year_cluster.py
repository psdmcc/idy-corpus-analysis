import pandas as pd

clusters = pd.read_csv(
    "data/analysis/canonical_transcripts_clustered.csv"
)

meta = pd.read_csv(
    "data/analysis/master_corpus_registry_v3.csv"
)

# merge on video_id
df = clusters.merge(
    meta[
        [
            "video_id",
            "title",
            "channel",
            "upload_date"
        ]
    ],
    on="video_id",
    how="left"
)

print("Rows:", len(df))
print("Missing dates:", df["upload_date"].isna().sum())

# extract year
df["year"] = pd.to_datetime(
    df["upload_date"].astype(str),
    format="%Y%m%d",
    errors="coerce"
).dt.year

# year x cluster table
table = pd.crosstab(
    df["year"],
    df["cluster"]
)

print("\nYEAR × CLUSTER")
print(table)

table.to_csv(
    "data/analysis/year_cluster_table.csv"
)

# save merged version for future work
df.to_csv(
    "data/analysis/canonical_transcripts_clustered_meta.csv",
    index=False
)

print("\nSaved:")
print("data/analysis/year_cluster_table.csv")
print("data/analysis/canonical_transcripts_clustered_meta.csv")
