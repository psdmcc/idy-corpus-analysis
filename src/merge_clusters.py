import pandas as pd

registry = pd.read_csv(
    "data/analysis/master_corpus_registry_v3.csv"
)

clusters = pd.read_csv(
    "data/analysis/canonical_transcripts_clustered.csv"
)

df = registry.merge(
    clusters[["video_id", "cluster"]],
    on="video_id",
    how="inner"
)

df.to_csv(
    "data/analysis/cluster_interpretation.csv",
    index=False
)

print(len(df))
print(df["cluster"].value_counts().sort_index())
