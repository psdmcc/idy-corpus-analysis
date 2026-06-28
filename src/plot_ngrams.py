import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

INPUT_FILE = Path("data/ngram_results.csv")
OUTPUT_IMAGE = Path("figures/yoga_sustainability_ngrams.png")

def generate_automated_plot():
    if not INPUT_FILE.exists():
        print(f"Error: {INPUT_FILE} not found. Please run your analyzer first.")
        return

    # Load the real dataset generated from your 1,758 documents
    df = pd.read_csv(INPUT_FILE)
    
    if df.empty:
        print("The ngram_results.csv file is empty. No data to plot.")
        return

    # Group by type and phrase, summing frequencies to catch duplicates
    df = df.groupby(["type", "phrase"])["frequency"].sum().reset_index()
    df = df.sort_values(by="frequency", ascending=True).tail(10)

    # Apply professional academic styling
    plt.style.use("default")
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    
    # Elegant forest green and slate palette for academic publishing
    colors = ["#1b4d3e" if t == "tri-gram" else "#2e6f40" for t in df["type"]]
    bars = ax.barh(df["phrase"], df["frequency"], color=colors, height=0.5, edgecolor="#333333", linewidth=0.8)
    
    # Structural titles and labels
    ax.set_title("Empirical Distribution of Yogic and Environmental Discourses", fontsize=13, fontweight="bold", pad=20, color="#111111")
    ax.set_xlabel("Absolute Phrase Frequency across 1,758 Indexed Text Documents", fontsize=10, fontweight="bold", labelpad=10)
    
    # Dynamically scale axis padding based on maximum values
    max_val = df["frequency"].max()
    ax.set_xlim(0, max_val * 1.25)
    ax.xaxis.get_major_locator().set_params(integer=True)
    
    # Overlay exact counts on top of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + (max_val * 0.01), bar.get_y() + bar.get_height()/2, f'{int(width)}', 
                va='center', ha='left', fontsize=10, fontweight='bold', color='#222222')
                
    # Remove borders
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
        
    plt.tight_layout()
    OUTPUT_IMAGE.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_IMAGE, bbox_inches="tight")
    print(f"Success! Scaled chart generated across 1,758 files: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    generate_automated_plot()
