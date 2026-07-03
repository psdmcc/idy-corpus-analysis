import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

CSV_FILENAME = "NIH_yoga_metadata_2014_2026.csv"

# ==========================================
# REFINED HIGH-PRECISION FILTERING MATRIX
# ==========================================
# We use targeted phrases to ensure we catch social, ecological, and structural angles.
GOVERNANCE_KEYWORDS = [
    "governance", "policy", "regulation", "ministry", "legislation", 
    "curriculum", "public health policy", "educational system", "institutional",
    "government", "municipal", "legal framework", "credentialing", "standardization"
]

SUSTAINABILITY_KEYWORDS = [
    "sustainability", "sustainable", "ecology", "ecological", "environmental", 
    "green spaces", "climate change", "nature-based", "eco-friendly", 
    "conservation", "sustainable development", "planetary health"
]

def analyze_niche_literature():
    print("Loading master dataset...")
    df = pd.read_csv(CSV_FILENAME)
    
    # Clean years safely (ignore future projections beyond 2026)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df = df[(df["Year"] >= 2014) & (df["Year"] <= 2026)]
    df["Year"] = df["Year"].astype(int)
    
    # Merge text columns for deeper analysis
    df["Search_Text"] = (df["Title"].fillna("") + " " + df["Abstract"].fillna("")).str.lower()
    
    # Apply boolean masks to isolate clean subsets
    gov_mask = df["Search_Text"].apply(lambda text: any(kw in text for kw in GOVERNANCE_KEYWORDS))
    sust_mask = df["Search_Text"].apply(lambda text: any(kw in text for kw in SUSTAINABILITY_KEYWORDS))
    
    # Assign exclusive target segments (prioritize sustainability if a paper hits both)
    df["Target_Segment"] = "Other Research"
    df.loc[gov_mask, "Target_Segment"] = "Governance & Policy"
    df.loc[sust_mask, "Target_Segment"] = "Sustainability & Ecology"
    
    # Filter dataset down to JUST our target literature
    niche_df = df[df["Target_Segment"] != "Other Research"].copy()
    
    print(f"\nFound {len(niche_df[niche_df['Target_Segment'] == 'Governance & Policy'])} pure Governance papers.")
    print(f"Found {len(niche_df[niche_df['Target_Segment'] == 'Sustainability & Ecology'])} pure Sustainability papers.")
    
    # Save the isolated metadata subsets to separate files for your review
    niche_df[niche_df['Target_Segment'] == 'Governance & Policy'].to_csv("yoga_governance_metadata.csv", index=False)
    niche_df[niche_df['Target_Segment'] == 'Sustainability & Ecology'].to_csv("yoga_sustainability_metadata.csv", index=False)
    print("Saved 'yoga_governance_metadata.csv' and 'yoga_sustainability_metadata.csv'.")
    
    # Calculate yearly volumes
    counts_timeline = niche_df.groupby(["Year", "Target_Segment"]).size().unstack(fill_value=0)
    
    # Ensure all years from 2014 to 2026 exist in our index for a smooth line chart
    all_years = pd.Index(range(2014, 2027), name="Year")
    counts_timeline = counts_timeline.reindex(all_years, fill_value=0)
    
    # =========================================================
    # VISUALIZATION 1: DUAL AXIS TIMELINE (GROWTH TRACKING)
    # =========================================================
    sns.set_theme(style="whitegrid")
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    color_gov = '#2b5c8f'  # Slate Blue
    color_sust = '#2e8b57' # Sea Green
    
    # Plot Governance on left Y-axis
    line1 = ax1.plot(counts_timeline.index, counts_timeline["Governance & Policy"], 
                     color=color_gov, marker="o", linewidth=3, label="Governance & Policy (Left Axis)")
    ax1.set_xlabel("Year of Publication", fontsize=12)
    ax1.set_ylabel("Governance Articles Count", color=color_gov, fontsize=12)
    ax1.tick_params(axis='y', labelcolor=color_gov)
    
    # Plot Sustainability on right Y-axis (since counts are lower, this shows true growth slope)
    ax2 = ax1.twinx()
    line2 = ax2.plot(counts_timeline.index, counts_timeline["Sustainability & Ecology"], 
                     color=color_sust, marker="s", linewidth=3, linestyle="--", label="Sustainability & Ecology (Right Axis)")
    ax2.set_ylabel("Sustainability Articles Count", color=color_sust, fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color_sust)
    
    plt.title("Growth & Differentiation Trajectory of Non-Medical Yoga Literature (2014–2026)", fontsize=14, fontweight="bold", pad=15)
    ax1.set_xticks(range(2014, 2027))
    
    # Combine legends from both axes
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper left")
    
    plt.tight_layout()
    plt.savefig("niche_growth_trajectory.png", dpi=300)
    plt.close()
    
    # =========================================================
    # DATA EXPLORATION: TOP JOURNALS DRIVING DIFFERENTIATION
    # =========================================================
    print("\n" + "="*50)
    print("TOP 5 JOURNALS PUBLISHING YOGA GOVERNANCE:")
    print("="*50)
    print(niche_df[niche_df['Target_Segment'] == 'Governance & Policy']['Journal'].value_counts().head(5))
    
    print("\n" + "="*50)
    print("TOP 5 JOURNALS PUBLISHING YOGA SUSTAINABILITY:")
    print("="*50)
    print(niche_df[niche_df['Target_Segment'] == 'Sustainability & Ecology']['Journal'].value_counts().head(5))

if __name__ == "__main__":
    analyze_niche_literature()
