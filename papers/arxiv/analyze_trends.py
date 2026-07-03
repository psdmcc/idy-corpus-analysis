import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

CSV_FILENAME = "NIH_yoga_metadata_2014_2026.csv"
TREND_FIGURE_FILENAME = "yoga_trends_2014_2026.png"

# ==========================================
# EXPANDED YOGA RESEARCH CATEGORIES
# ==========================================
TOPIC_KEYWORDS = {
    "Clinical Health & Therapy": [
        "patient", "trial", "pain", "anxiety", "depression", "cancer", 
        "clinical", "therapy", "treatment", "stress", "intervention", 
        "rehabilitation", "symptom", "mental health", "disorder"
    ],
    "Tourism & Lifestyle": [
        "tourism", "travel", "retreat", "wellness", "hotel", "destination", 
        "leisure", "consumer", "hospitality", "vacation", "industry", 
        "spa", "well-being", "lifestyle", "commercial"
    ],
    "Governance, Policy & Education": [
        "governance", "policy", "education", "school", "curriculum", 
        "government", "regulation", "ministry", "legal", "politics", 
        "institution", "guideline", "public health", "program", "student"
    ],
    "Sustainability & Ecology": [
        "sustainability", "sustainable", "ecology", "environment", "green", 
        "nature", "climate", "conservation", "eco-", "organic", "resource", 
        "development", "agricultural", "planet"
    ],
    "Biomechanics & Physiology": [
        "muscle", "heart", "brain", "spine", "posture", "flexibility", 
        "heart rate", "physiological", "cortex", "motor", "balance", 
        "kinematic", "respiratory", "breathing", "anatomy"
    ]
}


def assign_clean_topic(text):
    """Categorizes an article based on keyword counts to minimize overlap."""
    if not isinstance(text, str):
        return "Other / General Yoga"

    text = text.lower()
    scores = {topic: 0 for topic in TOPIC_KEYWORDS}

    # Count keyword matches for each category
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            scores[topic] += text.count(keyword)

    # Find the category with the highest match score
    max_score = max(scores.values())
    if max_score == 0:
        return "Other / General Yoga"

    # Return the highest-scoring category
    return max(scores, key=scores.get)


def generate_trends(csv_path):
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)

    # 1. Clean up and filter publication years
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    # Drop rows without years or outside our target window
    df = df[(df["Year"] >= 2014) & (df["Year"] <= 2026)]
    df["Year"] = df["Year"].astype(int)

    # 2. Combine Title and Abstract for robust scanning
    df["Full_Text"] = (df["Title"].fillna("") + " " + df["Abstract"].fillna(""))

    # 3. Categorize papers cleanly
    print("Applying updated non-overlapping categorization rules...")
    df["Clean_Topic"] = df["Full_Text"].apply(assign_clean_topic)

    # 4. Create a pivot table: Counts of topics per year
    trend_data = (
        df.groupby(["Year", "Clean_Topic"]).size().unstack(fill_value=0)
    )

    # 5. Build the trend visual
    print("Generating trend-over-time visualization...")
    plt.figure(figsize=(12, 7))
    sns.set_theme(style="whitegrid")

    # Plot a line for every category
    for column in trend_data.columns:
        # Avoid cluttering the lines with 'Other' if it's too dominant
        linewidth = 3 if column != "Other / General Yoga" else 1.5
        linestyle = "-" if column != "Other / General Yoga" else "--"

        plt.plot(
            trend_data.index,
            trend_data[column],
            marker="o",
            linewidth=linewidth,
            linestyle=linestyle,
            label=column,
        )

    plt.title(
        "Evolution of Yoga Research Fields Over Time (2014–2026)",
        fontsize=16,
        fontweight="bold",
        pad=15,
    )
    plt.xlabel("Year of Publication", fontsize=12)
    plt.ylabel("Number of Published Articles", fontsize=12)
    plt.xticks(np.arange(2014, 2027, 1))  # Ensure every year is labeled

    # Position the legend outside the chart layout to keep it clean
    plt.legend(
        title="Research Domains",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0,
    )
    plt.tight_layout()

    # Save to disk
    plt.savefig(TREND_FIGURE_FILENAME, dpi=300)
    print(f"🎉 Cleaned trend graph successfully saved as '{TREND_FIGURE_FILENAME}'!")

    # Show a quick summary text breakdown in terminal
    print("\nTotal papers matching each category overall:")
    print(df["Clean_Topic"].value_counts())


if __name__ == "__main__":
    if os.path.exists(CSV_FILENAME):
        generate_trends(CSV_FILENAME)
    else:
        print(f"Error: Could not find '{CSV_FILENAME}' in this folder.")
