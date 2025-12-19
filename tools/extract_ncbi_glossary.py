import requests
from bs4 import BeautifulSoup
import json
from time import sleep

URL = "https://www.ncbi.nlm.nih.gov/datasets/docs/v2/glossary/"
OUT_JSON = "tools/extracted/ncbi_glossary.json"

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

entries = []
for item in soup.select("dl dt"):
    term = item.get_text(strip=True)
    dd = item.find_next_sibling("dd")
    definition = dd.get_text(strip=True) if dd else ""
    if term and definition:
        entries.append({
            "term": term,
            "definition": definition,
            "field": "General Genetics",
            "difficulty": "Intermediate",
            "usage_example": "",
            "synonyms": [],
            "related_terms": [],
            "methods": [],
            "applications": [],
            "references": [{"source": "NCBI", "url": URL}],
            "provenance": "ncbi_glossary"
        })
    sleep(0.1)

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(entries)} terms to {OUT_JSON}")
