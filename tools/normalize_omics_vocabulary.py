import json
import re
from pathlib import Path

# ================= CONFIG =================
INPUT_JSON = Path("data/omics_vocabulary.json")
OUTPUT_JSON = Path("data/omics_vocabulary_clean.json")

# ================= HELPERS =================
CONTEXT_PATTERN = re.compile(
    r"\s*\((clinical\/research context|analysis context|omics context)\)",
    re.IGNORECASE
)

def normalize_term(term: str) -> str:
    """
    Remove artificial context suffixes from term names.
    """
    term = CONTEXT_PATTERN.sub("", term)
    return term.strip()

def extract_context(term: str) -> list:
    """
    Extract context tags from term name.
    """
    contexts = []
    term_lower = term.lower()
    if "clinical" in term_lower or "research" in term_lower:
        contexts.append("clinical/research")
    if "omics context" in term_lower:
        contexts.append("omics")
    if "analysis context" in term_lower:
        contexts.append("analysis")
    return contexts

def dedupe_list(items):
    return sorted(set(i for i in items if i))

# ================= LOAD =================
raw_data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))

# ================= NORMALIZE =================
merged = {}

for entry in raw_data:
    raw_term = entry.get("term", "").strip()
    if not raw_term:
        continue

    canonical_term = normalize_term(raw_term)
    contexts = extract_context(raw_term)

    if canonical_term not in merged:
        merged[canonical_term] = {
            "term": canonical_term,
            "definition": entry.get("definition", "").strip(),
            "field": entry.get("field", "").strip(),
            "usage_example": entry.get("usage_example", "").strip(),
            "synonyms": [],
            "difficulty": entry.get("difficulty", "").strip(),
            "contexts": [],
            "provenance": set()
        }

    # ---- Merge definition (keep longest) ----
    if len(entry.get("definition", "")) > len(merged[canonical_term]["definition"]):
        merged[canonical_term]["definition"] = entry["definition"].strip()

    # ---- Merge synonyms ----
    merged[canonical_term]["synonyms"].extend(entry.get("synonyms", []))

    # ---- Merge contexts ----
    merged[canonical_term]["contexts"].extend(contexts)

    # ---- Merge provenance ----
    for p in entry.get("provenance", "").split(","):
        if p.strip():
            merged[canonical_term]["provenance"].add(p.strip())

# ================= FINAL CLEANUP =================
final_vocab = []

for item in merged.values():
    item["synonyms"] = dedupe_list(item["synonyms"])
    item["contexts"] = dedupe_list(item["contexts"])
    item["provenance"] = ",".join(sorted(item["provenance"]))

    # Remove empty optional fields
    if not item["contexts"]:
        del item["contexts"]

    final_vocab.append(item)

# Sort alphabetically
final_vocab = sorted(final_vocab, key=lambda x: x["term"].lower())

# ================= WRITE =================
OUTPUT_JSON.write_text(
    json.dumps(final_vocab, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("✅ Omics vocabulary normalized successfully")
print(f"📥 Input entries : {len(raw_data)}")
print(f"📤 Output entries: {len(final_vocab)}")
print(f"💾 Written to    : {OUTPUT_JSON}")
