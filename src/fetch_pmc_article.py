import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
import ssl  # Fixed: Added to bypass macOS certificate issues

OUTPUT_DIR = Path("data/corpus_expansion")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "PMC12931643_ecotherapy.txt"

def fetch_pmc_text():
    print("Initiating direct API fetch for PMC12931643...")
    api_url = "https://nih.gov"
    
    try:
        # Fixed: Explicitly ignore the self-signed certificate barrier
        context = ssl._create_unverified_context()
        req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
        
        with urllib.request.urlopen(req, context=context) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        text_content = []
        
        for body in root.iter('body'):
            for p in body.iter('p'):
                if p.text:
                    text_content.append(p.text)
                    
        full_text = "\n\n".join(text_content)
        
        if full_text:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"Success! Clean text extracted and saved to: {OUTPUT_FILE.name}")
        else:
            print("API responded, but could not extract paragraphs from body fields.")
            
    except Exception as e:
        print(f"API endpoint connection failure: {e}")

if __name__ == "__main__":
    fetch_pmc_text()
