import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

print("Loading metadata...")
df = pd.read_csv("data/analysis/canonical_transcripts_v2.csv")

print("Loading transcripts...")

df["text"] = df["filepath"].apply(
    lambda p: open(p, encoding="utf-8").read()
)

print("Building TF-IDF matrix...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X = vectorizer.fit_transform(df["text"])

print("Clustering...")

kmeans = KMeans(
    n_clusters=10,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X)

print(df.groupby("cluster").size())

df.to_csv(
    "data/analysis/canonical_transcripts_clustered.csv",
    index=False
)

print("Saved:")
print("data/analysis/canonical_transcripts_clustered.csv")
