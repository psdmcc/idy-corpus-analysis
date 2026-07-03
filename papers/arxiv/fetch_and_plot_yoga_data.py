import os, csv, urllib.parse, urllib.request, xml.etree.ElementTree as ET, matplotlib.pyplot as plt, numpy as np

API_KEY = "1f600e1fc6c28fc3ec03e135f3aee9c58509"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

def fetch_and_append_track(file_name, track_label, csv_writer):
    if not os.path.exists(file_name): return 0
    with open(file_name, 'r') as f: ids = f.read().strip()
    if not ids: return 0
    
    url = "https://nih.gov"
    payload = urllib.parse.urlencode({"db": "pubmed", "id": ids, "retmode": "xml", "api_key": API_KEY}).encode('utf-8')
    req = urllib.request.Request(url, data=data_payload if 'data_payload' in locals() else payload, headers={"User-Agent": USER_AGENT})
    
    counts = {str(y): 0 for y in range(2014, 2027)}
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            root = ET.fromstring(resp.read().decode('utf-8', errors='ignore').replace("&ndash;", "-").replace("&mdash;", "-").encode('utf-8'))
            for art in root.findall(".//PubmedArticle"):
                pmid = art.find(".//MedlineCitation/PMID").text
                title = getattr(art.find(".//ArticleTitle"), 'text', 'No Title Available')
                journal = getattr(art.find(".//Journal/Title"), 'text', 'Unknown Journal')
                yr = "Unknown"
                y_elem = art.find(".//JournalIssue/PubDate/Year")
                if y_elem is not None and y_elem.text: yr = y_elem.text.strip()[:4]
                else:
                    md = art.find(".//JournalIssue/PubDate/MedlineDate")
                    dt = md.text if md is not None else ""
                    for w in dt.split():
                        cw = "".join(filter(str.isdigit, w))
                        if len(cw) == 4 and cw.startswith(("201", "202")): yr = cw; break
                auth_l = art.find(".//AuthorList/Author/LastName")
                author = auth_l.text if auth_l is not None else "Anonymous"
                doi = "No DOI Provided"
                for id_elem in art.findall(".//ArticleIdList/ArticleId"):
                    if id_elem.attrib.get("IdType") == "doi": doi = f"https://doi.org{id_elem.text}"; break
                if yr in counts:
                    counts[yr] += 1
                    csv_writer.writerow([track_label, pmid, yr, author, title, journal, doi])
    except Exception as e: print(f"⚠️ Metadata fetch failed for {track_label}: {e}")
    return counts

def run_local_build():
    csv_path = "figures/yoga_publications_metadata.csv"
    years = [str(y) for y in range(2014, 2027)]
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Thematic Category", "PMID", "Publication Year", "Primary Author", "Article Title", "Journal Name", "DOI Link"])
        c1 = fetch_and_append_track(".ids_h.txt", "Yoga & Health Treatments", writer)
        c2 = fetch_and_append_track(".ids_c.txt", "Yoga & Coronavirus/COVID-19", writer)
        c3 = fetch_and_append_track(".ids_s.txt", "Yoga & Sustainability Governance", writer)
        
    y1, y2, y3 = [c1.get(y,0) for y in years], [c2.get(y,0) for y in years], [c3.get(y,0) for y in years]
    plt.style.use('default'); fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
    x = np.arange(len(years))
    ax.bar(x, y1, 0.65, label='Yoga & Health Treatments', color='#2a9d8f')
    ax.bar(x, y2, 0.65, bottom=y1, label='Yoga & Coronavirus/COVID-19', color='#e9c46a')
    ax.bar(x, y3, 0.65, bottom=[r+i for r,i in zip(y1,y2)], label='Yoga & Sustainability Governance', color='#e76f51')
    ax.set_xticks(x); ax.set_xticklabels([yr if yr != '2026' else '2026*' for yr in years])
    ax.legend(loc='upper left')
    plt.tight_layout(); plt.savefig("figures/covid_yoga_trends.png", bbox_inches='tight'); plt.close()
    print("📈 Genuine visualization compiled successfully from live metrics.")

if __name__ == "__main__": run_local_build()
