"""
Daily challenge system
"""

import streamlit as st
from datetime import datetime
import random

def render_daily_challenge(nlp):
    """Render daily challenge"""
    st.header("🎯 Daily Challenge")
    st.caption("Complete daily challenges to maintain your streak!")
    
    today = datetime.now().date()
    daily_state = st.session_state.get('daily_challenge', {})
    
    if daily_state.get('date') != today:
        # Generate new challenge
        challenge_type = random.choice(['vocab_quiz', 'sentence_correction'])
        daily_state = {
            'date': today,
            'type': challenge_type,
            'completed': False,
            'score': 0
        }
        st.session_state.daily_challenge = daily_state
    
    if not daily_state['completed']:
        if daily_state['type'] == 'vocab_quiz':
            render_vocab_quiz_challenge()
        else:
            render_sentence_correction_challenge(nlp)
    else:
        st.success(f"✅ Today's challenge completed! Score: {daily_state['score']}/10")
        st.balloons()
        st.info("Come back tomorrow for a new challenge!")

def render_vocab_quiz_challenge():
    """Quick vocabulary quiz"""
    st.subheader("Vocabulary Quiz Challenge")
    # Implementation similar to quiz mode
    st.info("Quick 10-question vocabulary quiz!")
    
def render_sentence_correction_challenge(nlp):
    """Sentence correction challenge"""
    st.subheader("Sentence Correction Challenge")
    st.info("Identify and correct errors in scientific sentences!")