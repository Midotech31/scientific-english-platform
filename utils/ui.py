"""
UI Components for OmicsLingua
Author: Dr. MERZOUG Mohamed (ESSBO)
"""

import streamlit as st

def load_css():
    st.markdown("""
    <style>
    .term-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

def term_card(term):
    st.markdown(f"""
    <div class="term-card">
        <h4>{term['term']}</h4>
        <p><strong>Definition:</strong> {term['definition']}</p>
        <p><strong>Domain:</strong> {term['field']} | <strong>Level:</strong> {term['difficulty']}</p>
        <p><em>{term.get('usage_example','')}</em></p>
    </div>
    """, unsafe_allow_html=True)