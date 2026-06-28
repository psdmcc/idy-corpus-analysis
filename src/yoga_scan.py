from pathlib import Path
import pandas as pd
import re

BASE_DIR = "./data/analysis/clusters"

PATTERNS = [
    r"\byoga\b",
    r"yoga day",
    r"international yoga day",
    r"\bIDY\b",
    r"yoga diwas"
]

regex = re.compile("|".join(PATTERNS), re.IGNORECASE)

results = []

for file in Path(BASE_DIR).glob("cluster_*.csv"):
    df = pd.read_csv(file, on_bad_lines="skip")

    # combine all columns into one text field per row
    text_series = df.astype(str).agg(" ".join, axis=1)

    mask = text_series.str.contains(regex, na=False)

    yoga_df = df[mask].copy()

    # --- discourse quality classification ---
    def classify(text):
        text = str(text)

        if len(text) < 50:
            return "fragment"
        if "subscribe" in text.lower() or "thank you" in text.lower():
            return "boilerplate"
        if len(text.split()) > 80:
            return "full_discourse"
        return "medium"

    if len(yoga_df) > 0:
        sample_text = yoga_df.iloc[:, 0].astype(str)
        yoga_df["quality"] = sample_text.apply(classify)

        yoga_df.to_csv(f"yoga_hits_{file.stem}.csv", index=False)

    results.append({
        "cluster": file.name,
        "total_rows": len(df),
        "yoga_rows": len(yoga_df),
        "yoga_ratio": len(yoga_df) / len(df) if len(df) else 0,
        "full_discourse_rows": (yoga_df["quality"] == "full_discourse").sum() if len(yoga_df) else 0,
        "fragment_rows": (yoga_df["quality"] == "fragment").sum() if len(yoga_df) else 0,
        "boilerplate_rows": (yoga_df["quality"] == "boilerplate").sum() if len(yoga_df) else 0
    })

summary = pd.DataFrame(results).sort_values("yoga_rows", ascending=False)

print("\n=== FULL YOGA DAY CORPUS ANALYSIS ===\n")
print(summary)

summary.to_csv("yt_full_corpus_yoga_analysis.csv", index=False)
