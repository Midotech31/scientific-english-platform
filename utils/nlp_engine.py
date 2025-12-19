import streamlit as st
import spacy
from textblob import TextBlob
import subprocess
import sys

@st.cache_resource
def load_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

def analyze_text(text, nlp):
    return nlp(text)

def check_passive_voice(doc):
    passive_sentences = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "nsubjpass":
                passive_sentences.append(sent.text)
                break
    return list(set(passive_sentences))

def get_readability_score(text):
    blob = TextBlob(text)
    if not blob.sentences: return 0
    return round(100 - (len(blob.words) / len(blob.sentences) * 1.5), 1)
