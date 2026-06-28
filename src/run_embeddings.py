import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

# 1. LOAD DATA
df = pd.read_csv("data/analysis/canonical_transcripts_v2.csv")

print("Loaded:", len(df))

# 2. LOAD TEXT
def load_text(row):
    try:
        with open(row["filepath"], "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

df["text"] = df.apply(load_text, axis=1)

print("Text loaded")

# 3. EMBEDDINGS
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding...")
embeddings = model.encode(df["text"].fillna("").tolist(), show_progress_bar=True)

print("Embedding shape:", len(embeddings), len(embeddings[0]))

# 4. CLUSTERING
print("Clustering...")
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

df["cluster"] = kmeans.fit_predict(embeddings)

# 5. OUTPUT
print(df[["video_id", "cluster"]].head())
