import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.embl.org/ells/teachingbase/ells-glossary/"
OUT_JSON = "tools/extracted/embl_ebi_glossary.json"

r = requests.get(URL)
soup = BeautifulSoup(r.text, "html.parser")

entries = []
for li in soup.select("li"):
    text = li.get_text(" ", strip=True)
    if "–" in text:
        term, definition = text.split("–", 1)
        entries.append({
            "term": term.strip(),
            "definition": definition.strip(),
            "field": "Omics & Bioinformatics",
            "difficulty": "Intermediate",
            "usage_example": "",
            "synonyms": [],
            "related_terms": [],
            "methods": [],
            "applications": [],
            "references": [{"source": "EMBL-EBI", "url": URL}],
            "provenance": "embl_ebi_glossary"
        })

with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(entries)} terms to {OUT_JSON}")