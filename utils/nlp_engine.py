"""
NLP Engine for OmicsLingua
Author: Dr. MERZOUG Mohamed (ESSBO)
"""

import spacy
from textblob import TextBlob
import streamlit as st

@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

def analyze_text(text, nlp):
    return nlp(text)

def check_passive_voice(doc):
    return [s.text for s in doc.sents if any(t.dep_ == "nsubjpass" for t in s)]

def get_readability_score(text):
    blob = TextBlob(text)
    if not blob.sentences:
        return 0
    return round(100 - (len(blob.words) / len(blob.sentences) * 1.5), 1)