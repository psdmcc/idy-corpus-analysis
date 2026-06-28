import pandas as pd
from ontology import assign_ontology

df = pd.read_csv("data/analysis/canonical_transcripts_v2.csv")

df[["institution","modality"]] = df.apply(
    lambda r: pd.Series(assign_ontology(r)),
    axis=1
)

df.to_csv("data/analysis/canonical_transcripts_v3_annotated.csv", index=False)

print(df.head())
