import pandas as pd
import json
from pathlib import Path

# =================================================
# PATHS (CORRECTED FOR YOUR PROJECT STRUCTURE)
# =================================================

CSV_FILES = list(Path("CSV").glob("batch*_institutional_glossary.csv"))
print("CSV files found:", CSV_FILES)

JSON_OUT = Path("data/omics_vocabulary.json")

# =================================================
# LOAD EXISTING VOCABULARY (IF PRESENT)
# =================================================

existing_terms = []
if JSON_OUT.exists():
    existing_terms = json.loads(JSON_OUT.read_text(encoding="utf-8"))

# =================================================
# HELPER FUNCTIONS
# =================================================

def clean_string(value):
    """Normalize string values safely."""
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()

# =================================================
# READ CSV FILES
# =================================================

csv_entries = []

for csv_file in CSV_FILES:
    print(f"Reading {csv_file} ...")
    df = pd.read_csv(csv_file)

    for _, row in df.iterrows():
        term = clean_string(
            row.get("term") or
            row.get("Term") or
            row.get("TERM")
        )

        if not term:
            continue

        entry = {
            "term": term,
            "definition": clean_string(
                row.get("definition") or
                row.get("Definition") or
                ""
            ),
            "field": clean_string(
                row.get("field") or
                row.get("Field") or
                "General"
            ),
            "difficulty": clean_string(
                row.get("difficulty") or
                row.get("Difficulty") or
                "Intermediate"
            ),
            "usage_example": clean_string(
                row.get("usage_example") or
                row.get("Usage") or
                ""
            ),
            "synonyms": [
                s.strip()
                for s in clean_string(row.get("synonyms")).split(";")
                if s.strip()
            ],
            "related_terms": [],
            "methods": [],
            "applications": [],
            "references": [],
            "provenance": "imported_csv"
        }

        csv_entries.append(entry)

print(f"CSV entries found: {len(csv_entries)}")

# =================================================
# MERGE WITH EXISTING VOCABULARY (DEDUPLICATION)
# =================================================

def merge_entries(existing, new):
    merged = {e["term"].lower(): e for e in existing}

    for e in new:
        key = e["term"].lower()

        if key in merged:
            # Keep the longest definition
            if len(e["definition"]) > len(merged[key].get("definition", "")):
                merged[key]["definition"] = e["definition"]

            # Merge synonyms
            merged[key]["synonyms"] = list(
                set(merged[key].get("synonyms", []) + e.get("synonyms", []))
            )

            # Track provenance
            merged[key]["provenance"] = ",".join(
                filter(None, [
                    merged[key].get("provenance", ""),
                    e.get("provenance", "")
                ])
            )
        else:
            merged[key] = e

    return list(merged.values())

# =================================================
# WRITE FINAL JSON
# =================================================

result = merge_entries(existing_terms, csv_entries)

JSON_OUT.write_text(
    json.dumps(result, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"Saved merged vocabulary with {len(result)} entries at {JSON_OUT}")