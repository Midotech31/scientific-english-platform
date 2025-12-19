"""
Helper functions
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from pathlib import Path
import json

def init_session_state():
    """Initialize all session state variables"""
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {
            'vocab_mastered': set(),
            'vocab_learning': set(),
            'vocab_tracking': {},
            'reading_completed': [],
            'writing_sessions': 0,
            'total_time': 0,
            'last_session': None,
            'streak_days': 0,
            'achievement_unlocked': [],
            'activity_log': [],
            'quiz_history': [],
            'words_today': 0,
            'vocab_timeline': []
        }
    
    if 'learning_profile' not in st.session_state:
        st.session_state.learning_profile = {
            'level': 'intermediate',
            'focus_areas': ['Genomics'],
            'weak_topics': {},
            'preferred_mode': 'visual'
        }

def update_last_session():
    """Update last session timestamp"""
    st.session_state.user_progress['last_session'] = datetime.now().isoformat()

def check_daily_streak():
    """Check and update daily learning streak"""
    last_session = st.session_state.user_progress.get('last_session')
    
    if last_session:
        last_date = datetime.fromisoformat(last_session).date()
        today = datetime.now().date()
        days_diff = (today - last_date).days
        
        if days_diff == 1:
            # Consecutive day
            st.session_state.user_progress['streak_days'] += 1
        elif days_diff > 1:
            # Streak broken
            st.session_state.user_progress['streak_days'] = 1
    else:
        st.session_state.user_progress['streak_days'] = 1

def load_vocabulary_data():
    """Load vocabulary database"""
    vocab_file = Path("data/omics_vocabulary.csv")
    
    if vocab_file.exists():
        return pd.read_csv(vocab_file)
    else:
        # Return sample data
        return pd.DataFrame({
            'term': ['Genome', 'Transcriptome', 'Proteome', 'Metabolome', 'Metagenome'],
            'definition': [
                'The complete set of genetic material in an organism',
                'The complete set of RNA transcripts produced by the genome',
                'The entire set of proteins expressed by a genome',
                'The complete set of small-molecule chemicals found in a biological sample',
                'Genetic material recovered from environmental samples'
            ],
            'category': ['Genomics', 'Transcriptomics', 'Proteomics', 'Metabolomics', 'Metagenomics'],
            'difficulty': ['beginner', 'intermediate', 'intermediate', 'advanced', 'advanced'],
            'example': [
                'The human genome contains approximately 3 billion base pairs.',
                'RNA-seq is used to analyze the transcriptome.',
                'Mass spectrometry helps identify proteins in the proteome.',
                'The metabolome reflects the physiological state of a cell.',
                'Shotgun sequencing is used for metagenome analysis.'
            ],
            'phonetic': ['ˈdʒiːnəʊm', 'trænˈskrɪptəʊm', 'ˈprəʊtiːəʊm', 'məˈtæbələʊm', 'ˈmetəˌdʒiːnəʊm'],
            'etymology': [
                'From gene + -ome (complete set)',
                'From transcript + -ome',
                'From protein + -ome',
                'From metabolite + -ome',
                'From meta- (beyond) + genome'
            ],
            'syllables': ['ge-nome', 'tran-scrip-tome', 'pro-te-ome', 'me-tab-o-lome', 'meta-ge-nome']
        })

def calculate_next_review(term, difficulty):
    """Calculate next review date for spaced repetition"""
    intervals = {'easy': 7, 'medium': 3, 'hard': 1}
    days = intervals.get(difficulty, 3)
    return datetime.now() + timedelta(days=days)

def add_to_learning_list(term):
    """Add term to learning list"""
    st.session_state.user_progress['vocab_learning'].add(term)
    
    # Log activity
    activity = f"Added '{term}' to learning list - {datetime.now().strftime('%H:%M')}"
    st.session_state.user_progress['activity_log'].append(activity)