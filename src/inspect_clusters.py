import pandas as pd

df = pd.read_csv("data/analysis/canonical_transcripts_v2.csv")

df["text"] = df["filepath"].apply(
    lambda p: open(p, encoding="utf-8").read()
)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X = vectorizer.fit_transform(df["text"])

kmeans = KMeans(
    n_clusters=10,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X)

terms = vectorizer.get_feature_names_out()

for i in range(10):
    center = kmeans.cluster_centers_[i]
    top = center.argsort()[-20:][::-1]

    print("\n" + "=" * 60)
    print("CLUSTER", i)
    print("=" * 60)

    print(", ".join(terms[j] for j in top))
