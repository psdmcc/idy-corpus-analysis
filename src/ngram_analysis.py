import os
import re
from collections import Counter
from pathlib import Path
import pandas as pd

# Define paths matching your repository structure
INPUT_DIRS = [Path("papers_and_clusters"), Path("data")]
OUTPUT_FILE = Path("data/ngram_results.csv")

# Key terms to track for contextual intersection
TARGET_TERMS = ["sustainability", "climate", "sdg", "environment", "nature", "lifestyle"]

def clean_and_tokenize(text):
    """Cleans text and breaks it down into individual words."""
    text = text.lower()
    # Remove punctuation but preserve spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def generate_ngrams(words, n):
    """Generates a list of n-grams from a list of tokens."""
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

def analyze_corpus():
    all_text = ""
    file_count = 0
    
    # Read text data across your text files and subtitle vtt sheets
    for directory in INPUT_DIRS:
        if not directory.exists():
            continue
        for ext in ["*.txt", "*.vtt", "*.srt"]:
            for file_path in directory.rglob(ext):  # Fixed: changed glob to rglob
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        all_text += " " + f.read()
                        file_count += 1
                except Exception as e:
                    print(f"Skipping {file_path.name} due to read error: {e}")

    print(f"Successfully indexed {file_count} documents for analysis.")
    
    # Tokenize corpus
    tokens = clean_and_tokenize(all_text)
    
    # Generate N-Grams
    bigrams = generate_ngrams(tokens, 2)
    trigrams = generate_ngrams(tokens, 3)
    
    # Extract frequencies
    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)
    
    # Filter for N-grams that explicitly link 'yoga' to climate/sustainability keywords
    filtered_results = []
    
    print("\n--- Top Relevant Concepts Found in Corpus ---")
    for phrase, count in trigram_counts.most_common():
        if "yoga" in phrase and any(term in phrase for term in TARGET_TERMS):
            print(f"[{count} matches]: {phrase}")
            filtered_results.append({"type": "tri-gram", "phrase": phrase, "frequency": count})
            
    for phrase, count in bigram_counts.most_common():
        if "yoga" in phrase and any(term in phrase for term in TARGET_TERMS):
            filtered_results.append({"type": "bi-gram", "phrase": phrase, "frequency": count})

    # Save results directly to your data directory for presentation
    if filtered_results:
        df = pd.DataFrame(filtered_results)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nAnalysis complete. Clean results exported to: {OUTPUT_FILE}")
    else:
        print("\nNo direct intersections found in current file subset.")

if __name__ == "__main__":
    analyze_corpus()
