import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_distinct_themes(csv_path, target_name):
    df = pd.read_csv(csv_path)
    # Combine title and abstract
    text_data = (df["Title"].fillna("") + " " + df["Abstract"].fillna("")).str.lower()
    
    # Configure TF-IDF to find unique 2-word combinations (bigrams)
    # We remove 'yoga' and common medical terms to expose the structural topics
    custom_stop_words = ['yoga', 'asana', 'pranayama', 'study', 'participants', 'results', 'methods', 'clincial', 'patients', 'effects', 'group']
    
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(2, 3), # Catch 2 and 3 word phrases
        max_features=25
    )
    
    # Run matrix processing, ignoring our custom junk words
    processed_text = text_data.apply(lambda x: ' '.join([word for word in x.split() if word not in custom_stop_words]))
    
    tfidf_matrix = vectorizer.fit_transform(processed_text)
    feature_names = vectorizer.get_feature_names_out()
    
    # Calculate top scoring terms overall
    importance_scores = tfidf_matrix.sum(axis=0).A1
    top_phrases = sorted(zip(importance_scores, feature_names), reverse=True)[:10]
    
    print(f"\n🚀 TOP 10 SYSTEMIC THEMES IN: {target_name.upper()}")
    print("="*60)
    for score, phrase in top_phrases:
        print(f"• {phrase.title()}")

if __name__ == "__main__":
    extract_distinct_themes("yoga_governance_metadata.csv", "Governance & Policy")
    extract_distinct_themes("yoga_sustainability_metadata.csv", "Sustainability & Ecology")
