from pathlib import Path
import pandas as pd
import re
import numpy as np

CLUSTER_DIR = "data/analysis/clusters"

# ------------------------
# SAME DSI FUNCTION AS compute_dsi.py
# ------------------------

def compute_dsi(text):

    if not isinstance(text, str):
        return np.nan

    words = re.findall(r"\b\w+\b", text.lower())

    if len(words) < 5:
        return np.nan

    vocab = len(set(words))
    total = len(words)

    lexical_diversity = vocab / total

    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]

    sentence_count = max(len(sentences), 1)

    sentence_score = total / sentence_count

    freq = pd.Series(words).value_counts()

    repetition_penalty = ((freq - 1).clip(lower=0).sum()) / total

    dsi = (
        2 * lexical_diversity
        + (1 / (sentence_score + 1))
        - (1.5 * repetition_penalty)
    )

    return dsi

# ------------------------
# BUILD ROW DATASET
# ------------------------

rows = []

for file in Path(CLUSTER_DIR).glob("cluster_*.csv"):

    df = pd.read_csv(file)

    cluster_name = file.stem

    for _, row in df.iterrows():

        text = str(row.get("text", ""))

        rows.append({
            "video_id": row.get("video_id"),
            "cluster": cluster_name,
            "channel": row.get("channel"),
            "year": row.get("year"),
            "word_count": row.get("word_count"),
            "dsi": compute_dsi(text)
        })

out = pd.DataFrame(rows)

out.to_csv("dsi_rows.csv", index=False)

print()
print("Saved dsi_rows.csv")
print()
print(out.head())
print()
print("Rows:", len(out))
