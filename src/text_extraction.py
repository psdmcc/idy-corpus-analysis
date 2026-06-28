import pandas as pd
import json
from pathlib import Path

# =========================
# CONFIG
# =========================
CSV_PATH = "data/analysis/canonical_transcripts_clustered_meta.csv"

TEXT_COL = "text"
CLUSTER_COL = "cluster"

CLUSTERS = [0, 2, 4, 6]

OUTPUT_MODE = "sample"   # "sample" or "full"
SAMPLES_PER_CLUSTER = 20

MIN_TEXT_LENGTH = 500    # (1) length filtering threshold
RANDOM_STATE = 42

OUTPUT_DIR = Path("cluster_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(CSV_PATH)

print("Total rows:", len(df))
print("Cluster distribution:\n", df[CLUSTER_COL].value_counts())

# =========================
# (1) LENGTH FILTERING
# =========================
df = df[df[TEXT_COL].astype(str).str.len() >= MIN_TEXT_LENGTH]

print("\nAfter length filtering:", len(df))

# =========================
# EXTRACT FUNCTION
# =========================
def extract_clusters(df, clusters, mode="sample"):
    results = {}

    for c in clusters:
        subset = df[df[CLUSTER_COL] == c].copy()

        # =========================
        # (2) DETERMINISTIC ORDERING
        # =========================
        subset = subset.sort_values(by=TEXT_COL).reset_index(drop=True)

        if mode == "full":
            selected = subset

        elif mode == "sample":
            n = min(SAMPLES_PER_CLUSTER, len(subset))
            selected = subset.sample(n=n, random_state=RANDOM_STATE)

            # keep deterministic ordering AFTER sampling
            selected = selected.sort_values(by=TEXT_COL).reset_index(drop=True)

        else:
            raise ValueError("mode must be 'sample' or 'full'")

        results[c] = selected

    return results

results = extract_clusters(df, CLUSTERS, OUTPUT_MODE)

# =========================
# (3) EXPORT: TXT + JSON
# =========================
json_output = {}

for cluster_id, subset in results.items():

    texts = subset[TEXT_COL].astype(str).tolist()

    # ---- TXT export ----
    txt_path = OUTPUT_DIR / f"cluster_{cluster_id}_{OUTPUT_MODE}.txt"

    with open(txt_path, "w", encoding="utf-8") as f:
        for i, t in enumerate(texts):
            f.write(f"\n\n===== CLUSTER {cluster_id} | ITEM {i} =====\n\n")
            f.write(t)

    print(f"Saved TXT: {txt_path} ({len(texts)} items)")

    # ---- JSON export ----
    json_output[cluster_id] = {
        "n_items": len(texts),
        "texts": texts
    }

json_path = OUTPUT_DIR / f"clusters_{OUTPUT_MODE}.json"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

print(f"\nSaved JSON: {json_path}")
