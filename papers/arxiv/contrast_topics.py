import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

CSV_FILENAME = "NIH_yoga_metadata_2014_2026.csv"

def extract_contrasted_themes():
    print("Loading master dataset for comparative text contrast...")
    df = pd.read_csv(CSV_FILENAME)
    
    # 1. Standardize processing text
    df["Clean_Text"] = (df["Title"].fillna("") + " " + df["Abstract"].fillna("")).str.lower()
    
    # 2. Re-apply our strict masks to isolate pure target groups
    gov_phrases = ["governance", "policy", "regulation", "ministry", "legislation", "curriculum", "government", "institutional", "legal"]
    sust_phrases = ["sustainability", "sustainable", "ecology", "ecological", "environmental", "green", "climate", "conservation", "nature"]
    
    gov_mask = df["Clean_Text"].apply(lambda text: any(p in text for p in gov_phrases))
    sust_mask = df["Clean_Text"].apply(lambda text: any(p in text for p in sust_phrases))
    
    # 3. Create a strict clinical trial baseline group to contrast against
    clinical_mask = df["Clean_Text"].str.contains("randomized controlled|clinical trial|placebo|double-blind", case=False, na=False)
    
    # Isolate texts
    gov_text = df[gov_mask & ~clinical_mask]["Clean_Text"]
    sust_text = df[sust_mask & ~clinical_mask]["Clean_Text"]
    clinical_text = df[clinical_mask]["Clean_Text"]
    
    print(f"Analyzing {len(gov_text)} non-clinical Governance records.")
    print(f"Analyzing {len(sust_text)} non-clinical Sustainability records.")

    # 4. Use a Vectorizer to count 2-3 word phrases (Bigrams/Trigrams)
    # We add aggressive stop words to eliminate standard academic filler
    filler_words = [
        'yoga', 'asana', 'pranayama', 'study', 'participants', 'results', 'methods', 
        'effects', 'group', 'significantly', 'compared', 'conclusion', 'background',
        'health', 'mind', 'body', 'associated', 'meditation', 'practice', 'practices'
    ]
    
    vectorizer = CountVectorizer(
        stop_words='english', 
        ngram_range=(2, 3), 
        min_df=2
    )
    
    # Helper to calculate contrasted importance
    def get_unique_phrases(target_series, baseline_series):
        # Clean filler words out of raw texts
        def clean_filler(text):
            return ' '.join([w for w in text.split() if w not in filler_words])
            
        target_cleaned = target_series.apply(clean_filler)
        baseline_cleaned = baseline_series.apply(clean_filler)
        
        # Fit vectorizer on all text combined to get a shared vocabulary
        all_text = pd.concat([target_cleaned, baseline_cleaned])
        vectorizer.fit(all_text)
        
        # Count frequencies
        target_counts = vectorizer.transform(target_cleaned).sum(axis=0).A1
        baseline_counts = vectorizer.transform(baseline_cleaned).sum(axis=0).A1
        
        feature_names = vectorizer.get_feature_names_out()
        
        # Contrast Formula: Target Frequency minus Baseline Frequency
        # This penalizes phrases that keep popping up in standard medical trials
        contrast_scores = {}
        for idx, name in enumerate(feature_names):
            # Normalize scores by dataset sizes
            t_score = target_counts[idx] / max(1, len(target_series))
            b_score = baseline_counts[idx] / max(1, len(baseline_series))
            contrast_scores[name] = t_score - b_score
            
        # Sort and return top phrases
        sorted_phrases = sorted(contrast_scores.items(), key=lambda item: item[1], reverse=True)
        return [phrase.title() for phrase, score in sorted_phrases[:12]]

    # Run contrast engine
    gov_themes = get_unique_phrases(gov_text, clinical_text)
    sust_themes = get_unique_phrases(sust_text, clinical_text)
    
    # Print the clean results
    print("\n🟢 SYSTEMIC DIFFERENTIATION: GOVERNANCE & POLICY")
    print("="*60)
    for t in gov_themes: print(f"• {t}")
        
    print("\n🟢 SYSTEMIC DIFFERENTIATION: SUSTAINABILITY & ECOLOGY")
    print("="*60)
    for t in sust_themes: print(f"• {t}")

if __name__ == "__main__":
    extract_contrasted_themes()
