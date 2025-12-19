"""
NLP Engine for OmicsLingua
Author: Dr. MERZOUG Mohamed (ESSBO)
"""

import spacy
import streamlit as st

# -------------------------------------------------
# Load spaCy model once (cached)
# -------------------------------------------------
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")


# -------------------------------------------------
# Core NLP functions
# -------------------------------------------------
def analyze_text(text, nlp):
    """Run spaCy NLP pipeline on text."""
    return nlp(text)


def check_passive_voice(doc):
    """Detect sentences containing passive voice."""
    passive_sentences = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "nsubjpass":
                passive_sentences.append(sent.text)
                break
    return passive_sentences


def get_readability_score(doc):
    """
    Compute a simple academic readability score using spaCy only.
    Higher score = easier to read.
    """

    sentences = list(doc.sents)
    if not sentences:
        return 0

    words = [token for token in doc if token.is_alpha]
    if not words:
        return 0

    avg_words_per_sentence = len(words) / len(sentences)

    # Heuristic readability metric (academic-focused)
    score = max(0, 100 - avg_words_per_sentence * 1.5)
    return round(score, 1)