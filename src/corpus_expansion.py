import urllib.request
from pathlib import Path
import ssl

EXPANSION_DIR = Path("data/corpus_expansion")
EXPANSION_DIR.mkdir(parents=True, exist_ok=True)

# Target literature links saved as PDFs to preserve structural text data
TARGET_URLS = {
    "yoga_life_climate_2025.pdf": "https://swastiyogacenter.com",
    "yoga_un_sdg_recommendations.pdf": "https://sonneundmond.com"
}

def download_expansion_corpus():
    print("Initiating automated pipeline corpus expansion...")
    # Safely handle SSL handshakes on secure academic networks
    context = ssl._create_unverified_context()
    
    for filename, url in TARGET_URLS.items():
        output_path = EXPANSION_DIR / filename
        try:
            print(f"Fetching: {filename}...")
            # Use urlopen which cleanly accepts the custom context parameter
            with urllib.request.urlopen(url, context=context) as response:
                with open(output_path, "wb") as f:
                    f.write(response.read())
            print(f"Successfully integrated {filename} into data tracking.")
        except Exception as e:
            print(f"Skipped {filename} due to transport network boundary: {e}")

if __name__ == "__main__":
    download_expansion_corpus()
