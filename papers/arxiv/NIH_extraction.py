import os
import ssl
import certifi

# Tell your system to use Certifi's security credentials
os.environ["SSL_CERT_FILE"] = certifi.where()
ssl._create_default_https_context = ssl._create_default_https_context


import csv
import os
import time
import matplotlib.pyplot as plt
import pandas as pd
from Bio import Entrez
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

# ==========================================
# CONFIGURATION
# ==========================================
# Always provide your email and API key to prevent blocks and use higher rate limits
Entrez.email = "u4556787@anu.edu.au"  # Replace with your linked email
Entrez.api_key = "1f600e1fc6c28fc3ec03e135f3aee9c58509"  # Replace with your NCBI API key

SEARCH_QUERY = "yoga AND (2014[DP] : 2026[DP])"
CSV_FILENAME = "NIH_yoga_metadata_2014_2026.csv"
FIGURE_FILENAME = "NIH_extraction_figure.png"
MAX_RESULTS = 10000  # Adjust based on your needed dataset size
BATCH_SIZE = 50

def search_pubmed(query, max_results):
    """Searches PubMed and returns a list of web environment IDs."""
    print(f"Searching PubMed for: '{query}'...")
    handle = Entrez.esearch(
        db="pubmed", term=query, retmax=max_results, usehistory="y"
    )
    record = Entrez.read(handle)
    handle.close()
    print(f"Found {record['Count']} total matches. Fetching {max_results}...")
    return record


def fetch_metadata(search_record, batch_size=100):
    """Fetches full XML details in batches to respect API limits."""
    count = int(search_record["Count"])
    webenv = search_record["WebEnv"]
    query_key = search_record["QueryKey"]

    articles_data = []

    # Loop through results in batches
    for start in range(0, min(count, MAX_RESULTS), batch_size):
        print(f"Fetching records {start} to {start + batch_size}...")
        try:
            fetch_handle = Entrez.efetch(
                db="pubmed",
                retmode="xml",
                retstart=start,
                retmax=batch_size,
                webenv=webenv,
                query_key=query_key,
            )
            records = Entrez.read(fetch_handle)
            fetch_handle.close()

            for article in records["PubmedArticle"]:
                medline = article["MedlineCitation"]
                biblio = medline["Article"]

                # Extract ID
                pmid = str(medline["PMID"])

                # Extract Title
                title = biblio.get("ArticleTitle", "")

                # Extract Year
                pub_date = biblio.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
                year = pub_date.get("Year", "Unknown")
                if year == "Unknown" and "MedlineDate" in pub_date:
                    year = pub_date["MedlineDate"][:4]  # fallback for seasonal dates

                # Extract Journal
                journal = biblio.get("Journal", {}).get("Title", "")

                # Extract Abstract Text
                abstract = ""
                if "Abstract" in biblio and "AbstractText" in biblio["Abstract"]:
                    abstract = " ".join([str(t) for t in biblio["Abstract"]["AbstractText"]])

                articles_data.append(
                    {
                        "PMID": pmid,
                        "Title": title,
                        "Year": year,
                        "Journal": journal,
                        "Abstract": abstract,
                    }
                )

            # Polite pause to ensure compliance with NCBI limits
            time.sleep(0.2)

        except Exception as e:
            print(f"Error fetching batch starting at {start}: {e}")
            continue

    return articles_data


def generate_topic_figure(df, num_topics=5):
    """Uses TF-IDF and KMeans to cluster text into general topics and plots them."""
    print("Analyzing text to find general topics...")

    # Fill empty text columns to avoid failures
    df["Analysis_Text"] = (df["Title"] + " " + df["Abstract"]).fillna("")

    # Convert text to numeric matrix ignoring common English stop words
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df["Analysis_Text"])

    # Cluster papers into distinct groups
    kmeans = KMeans(n_clusters=num_topics, random_state=42, n_init=10)
    df["Topic_Cluster"] = kmeans.fit_predict(tfidf_matrix)

    # Identify top words for each cluster to dynamically name the topics
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()

    topic_labels = {}
    for i in range(num_topics):
        top_words = [terms[ind] for ind in order_centroids[i, :3]]
        # Create a user-friendly label name from top words
        topic_labels[i] = " + ".join(top_words).title()

    df["Topic_Label"] = df["Topic_Cluster"].map(topic_labels)

    # Plot data
    plt.figure(figsize=(10, 6))
    df["Topic_Label"].value_counts().plot(kind="barh", color="teal")
    plt.title("Distribution of Yoga Research Topics (2014-2026)", fontsize=14)
    plt.xlabel("Number of Published Articles")
    plt.ylabel("Generated Topic Clusters (Top Words)")
    plt.tight_layout()

    # Save visualization to disk
    plt.savefig(FIGURE_FILENAME, dpi=300)
    print(f"Figure saved successfully as '{FIGURE_FILENAME}'")


# ==========================================
# MAIN EXECUTION (FULL RUN WITH DOI)
# ==========================================
if __name__ == "__main__":
    # 1. Search NCBI Database
    search_rec = search_pubmed(SEARCH_QUERY, MAX_RESULTS)
    total_records = int(search_rec["Count"])
    
    # 2. Extract Data in chunks and write them directly to disk
    webenv = search_rec["WebEnv"]
    query_key = search_rec["QueryKey"]
    
    # Setup headers containing your new DOI field
    headers = ["PMID", "DOI", "Title", "Year", "Journal", "Abstract"]
    with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

    print(f"Starting full scrape of {total_records} records...")
    
    # Loop through all matching records using the configured BATCH_SIZE
    for start in range(0, min(total_records, MAX_RESULTS), BATCH_SIZE):
        print(f"Progress: Fetching records {start} to {start + BATCH_SIZE} of {total_records}...")
        try:
            fetch_handle = Entrez.efetch(
                db="pubmed",
                retmode="xml",
                retstart=start,
                retmax=BATCH_SIZE,
                webenv=webenv,
                query_key=query_key,
            )
            records = Entrez.read(fetch_handle)
            fetch_handle.close()

            batch_data = []
            for article in records["PubmedArticle"]:
                medline = article["MedlineCitation"]
                biblio = medline["Article"]

                pmid = str(medline["PMID"])
                title = biblio.get("ArticleTitle", "")
                
                pub_date = biblio.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {})
                year = pub_date.get("Year", "Unknown")
                if year == "Unknown" and "MedlineDate" in pub_date:
                    year = pub_date["MedlineDate"][:4]

                journal = biblio.get("Journal", {}).get("Title", "")

                abstract = ""
                if "Abstract" in biblio and "AbstractText" in biblio["Abstract"]:
                    abstract = " ".join([str(t) for t in biblio["Abstract"]["AbstractText"]])

                # --- DOI EXTRACTION LOGIC ---
                doi = ""
                if "ELocationID" in biblio:
                    for eloc in biblio["ELocationID"]:
                        if eloc.attributes.get("EIdType") == "doi":
                            doi = str(eloc)
                            break
                
                if not doi and "PubmedData" in article and "ArticleIdList" in article["PubmedData"]:
                    for art_id in article["PubmedData"]["ArticleIdList"]:
                        if art_id.attributes.get("IdType") == "doi":
                            doi = str(art_id)
                            break

                batch_data.append({
                    "PMID": pmid,
                    "DOI": doi,
                    "Title": title,
                    "Year": year,
                    "Journal": journal,
                    "Abstract": abstract
                })

            # Append this batch immediately to the CSV file
            with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writerows(batch_data)

            # Pause briefly to be a good API citizen
            time.sleep(0.3)

        except Exception as e:
            print(f"⚠️ Error or timeout fetching batch at {start}. Retrying next batch... Error: {e}")
            time.sleep(2)
            continue

    print(f"\n🎉 Success! All available records saved to '{CSV_FILENAME}'")

    # 3. Reload full dataset from disk to generate the updated figure
    print("Loading full CSV back into memory for visualization generation...")
    df_all = pd.read_csv(CSV_FILENAME)
    
    if not df_all.empty:
        generate_topic_figure(df_all, num_topics=7)
    else:
        print("CSV file is empty. Cannot generate figure.")
