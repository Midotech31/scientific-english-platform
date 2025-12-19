"""
NLP engine using spaCy with additional text analysis functions
"""

import spacy
import streamlit as st
from config import SPACY_MODEL
import textstat

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
    
    if not text or len(text.strip()) < 3:
        return None
    
    doc = nlp(text)
    return {
        'tokens': len([token for token in doc if not token.is_punct]),
        'sentences': len(list(doc.sents)),
        'entities': [(ent.text, ent.label_) for ent in doc.ents],
        'pos_tags': [(token.text, token.pos_) for token in doc if not token.is_space],
        'avg_sentence_length': len([token for token in doc if not token.is_punct]) / max(len(list(doc.sents)), 1)
    }

def check_passive_voice(text, nlp):
    """Detect passive voice constructions"""
    if not nlp or not text:
        return []
    
    doc = nlp(text)
    passive_sentences = []
    
    for sent in doc.sents:
        for token in sent:
            # Detect passive: auxiliary verb + past participle
            if token.dep_ == "auxpass":
                passive_sentences.append(sent.text)
                break
    
    return passive_sentences

def get_readability_score(text):
    """Calculate readability metrics"""
    if not text or len(text.strip()) < 10:
        return None
    
    try:
        return {
            'flesch_reading_ease': round(textstat.flesch_reading_ease(text), 1),
            'flesch_kincaid_grade': round(textstat.flesch_kincaid_grade(text), 1),
            'avg_sentence_length': round(textstat.avg_sentence_length(text), 1),
            'difficult_words': textstat.difficult_words(text),
            'reading_time_minutes': round(textstat.reading_time(text, ms_per_char=14.69) / 60, 1)
        }
    except Exception as e:
        st.error(f"Readability calculation error: {e}")
        return None

def extract_scientific_terms(text, nlp):
    """Extract scientific and technical terms"""
    if not nlp or not text:
        return []
    
    doc = nlp(text)
    scientific_terms = []
    
    # Look for noun phrases and technical entities
    for chunk in doc.noun_chunks:
        # Filter for potential scientific terms (capitalized or compound nouns)
        if len(chunk.text.split()) > 1 or chunk.root.pos_ == "NOUN":
            scientific_terms.append(chunk.text)
    
    return list(set(scientific_terms))

def check_grammar_basic(text, nlp):
    """Basic grammar checking"""
    if not nlp or not text:
        return []
    
    doc = nlp(text)
    issues = []
    
    # Check for common issues
    for token in doc:
        # Subject-verb agreement (simplified)
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            subjects = [child for child in token.children if child.dep_ == "nsubj"]
            if subjects:
                subject = subjects[0]
                # Basic check
                if subject.tag_ == "NNS" and token.tag_ not in ["VBP", "VBZ"]:
                    issues.append({
                        'type': 'subject_verb_agreement',
                        'text': f"{subject.text} {token.text}",
                        'suggestion': "Check subject-verb agreement"
                    })
    
    return issues