"""
NLP engine using spaCy
"""

import spacy
import streamlit as st
from config import SPACY_MODEL

@st.cache_resource
def load_model():
    """Load spaCy model"""
    try:
        nlp = spacy.load(SPACY_MODEL)
        return nlp
    except OSError:
        st.warning(f"Downloading {SPACY_MODEL}...")
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", SPACY_MODEL])
        nlp = spacy.load(SPACY_MODEL)
        return nlp

def analyze_text(text, nlp):
    """Analyze text with spaCy"""
    if not nlp:
        return None
    
    doc = nlp(text)
    return {
        'tokens': len([token for token in doc if not token.is_punct]),
        'sentences': len(list(doc.sents)),
        'entities': [(ent.text, ent.label_) for ent in doc.ents],
        'pos_tags': [(token.text, token.pos_) for token in doc if not token.is_space]
    }