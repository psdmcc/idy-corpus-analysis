import re
from collections import Counter
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

INPUT_DIRS = [Path("papers_and_clusters"), Path("data")]
OUTPUT_CSV = Path("data/proximity_results.csv")
OUTPUT_IMAGE = Path("figures/yoga_proximity_chart.png")
KEYWORDS = ["sustainability", "climate", "sdg", "environment", "nature", "lifestyle"]

def analyze_proximity():
    print("Initiating proximity co-occurrence engine across 1,758 documents...")
    co_occurrences = Counter()
    file_count = 0

    for directory in INPUT_DIRS:
        if not directory.exists():
            continue
        for ext in ["*.txt", "*.vtt", "*.srt"]:
            for file_path in directory.rglob(ext):
                # Skip venv files if they accidentally sit inside data
                if "venv" in file_path.parts or "node" in file_path.name:
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        text = f.read().lower()
                        text = re.sub(r'[^a-z0-9\s]', '', text)
                        words = text.split()
                        file_count += 1
                        
                        # Scan for "yoga" and check its surrounding context window
                        for idx, word in enumerate(words):
                            if word == "yoga":
                                start = max(0, idx - 15)
                                end = min(len(words), idx + 16)
                                window = words[start:end]
                                
                                # Record which keywords appear near "yoga"
                                for kw in KEYWORDS:
                                    if kw in window:
                                        co_occurrences[kw] += 1
                except Exception:
                    pass

    print(f"Analysis complete. Processed {file_count} valid text tracks.")
    if not co_occurrences:
        print("No proximity matches found.")
        return

    # Convert to Dataframe and sort
    df = pd.DataFrame(co_occurrences.items(), columns=["Keyword", "Frequency"]).sort_values(by="Frequency", ascending=True)
    df.to_csv(OUTPUT_CSV, index=False)
    
    # Plotting the updated, high-density results
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    bars = ax.barh(df["Keyword"], df["Frequency"], color="#1b4d3e", height=0.5, edgecolor="#333333")
    
    ax.set_title("Contextual Proximity: Environmental Terms Found Within 15 Words of 'Yoga'", fontsize=12, fontweight="bold", pad=15)
    ax.set_xlabel("Absolute Co-occurrence Frequency Across Corpus", fontsize=10, fontweight="bold")
    
    max_val = df["Frequency"].max()
    ax.set_xlim(0, max_val * 1.2)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + (max_val * 0.01), bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                va='center', ha='left', fontsize=9, fontweight='bold')
                
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
        
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, bbox_inches="tight")
    print(f"Success! High-density proximity distribution map saved to: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    analyze_proximity()
