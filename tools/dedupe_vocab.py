import json
from pathlib import Path

INPUT_DIR = Path("tools/extracted")
OUT_JSON = Path("data/omics_vocabulary_expanded.json")

all_entries = []

for f in INPUT_DIR.glob("*.json"):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        for entry in data:
            entry["provenance"] = entry.get("provenance", "") + f"|extracted_from_{f.stem}"
            all_entries.append(entry)
    except Exception as e:
        print("Skipping", f, e)

# Deduplicate by term
merged = {}
for ent in all_entries:
    key = ent.get("term", "").lower()
    existing = merged.get(key)
    if not existing:
        merged[key] = ent
    else:
        if len(ent.get("definition","")) > len(existing.get("definition","")):
            existing["definition"] = ent["definition"]
        existing["synonyms"] = list(set(existing.get("synonyms",[]) + ent.get("synonyms",[])))
        existing["references"] = list({json.dumps(r) for r in existing.get("references",[]) + ent.get("references",[])})

final_list = list(merged.values())
OUT_JSON.write_text(json.dumps(final_list, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Merged {len(final_list)} unique vocabulary entries to {OUT_JSON}")