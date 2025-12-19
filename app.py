"""
OmicsLingua — Scientific English Platform for Omics & Genetic Engineering

Author: Dr. MERZOUG Mohamed
Affiliation: Higher School of Biological Sciences of Oran (ESSBO)
Year: 2025
License: MIT
Version: 2.0.0 (Enhanced)
"""

import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Import modules
from modules.omics_vocabulary import OmicsVocabularySystem
from modules.omics_reading import OmicsReadingComprehension
from modules.omics_writing import render_omics_writing_assistant
from modules.dashboard import render_dashboard
from modules.daily_challenge import render_daily_challenge
from modules.progress_analytics import render_progress_analytics

# Import utilities
from utils.nlp_engine import load_model
from utils.ui import load_css, render_sidebar_profile
from utils.database import UserProgressDB
from utils.helpers import init_session_state, update_last_session, check_daily_streak

# Configure logging
logging.basicConfig(
    filename='omicslinga.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OmicsLingua | Scientific English Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- INITIALIZE STATE ----------------
init_session_state()

# ---------------- LOAD RESOURCES ----------------
@st.cache_resource(ttl=3600)
def get_nlp():
    """Load spaCy model with caching"""
    try:
        return load_model()
    except Exception as e:
        logger.error(f"Failed to load NLP model: {e}")
        st.error("Failed to load NLP engine. Some features may be limited.")
        return None

nlp = get_nlp()

# Load CSS
load_css()

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 3])
with col1:
    logo = Path("assets/MyEnglishApp Logo.png")
    if logo.exists():
        st.image(str(logo), width=450)

with col2:
    st.title("OmicsLingua")
    st.caption("🧬 The Reference Platform for Scientific English in Omics & Genetic Engineering")

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📚 OmicsLingua Platform")

# User Profile Section
render_sidebar_profile()

# Navigation
section = st.sidebar.radio(
    "Navigate to:",
    [
        "🏠 Dashboard",
        "🧬 Vocabulary Intelligence",
        "📖 Interactive Reading",
        "✍️ Writing Assistant",
        "📊 Progress Analytics",
        "🎯 Daily Challenge"
    ]
)

st.sidebar.markdown("---")

# Data Management
with st.sidebar.expander("💾 Data Management"):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export"):
            progress_json = json.dumps(
                st.session_state.user_progress, 
                default=str, 
                indent=2
            )
            st.download_button(
                "Download JSON",
                progress_json,
                file_name=f"omicslinga_progress_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        uploaded = st.file_uploader("📤 Import", type=['json'], label_visibility="collapsed")
        if uploaded:
            try:
                imported_data = json.load(uploaded)
                st.session_state.user_progress.update(imported_data)
                st.success("✅ Progress restored!")
                st.rerun()
            except Exception as e:
                st.error(f"Import failed: {e}")

# Developer Mode
if st.sidebar.checkbox("🔧 Developer Mode", value=False):
    if st.sidebar.button("Clear All Caches"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("Caches cleared!")
    
    st.sidebar.json(st.session_state.user_progress, expanded=False)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Author & Maintainer**  
    Dr. MERZOUG Mohamed  
    Lecturer – ESSBO  

    *Microbial Genomics · Bioinformatics · Scientific Education*
    
    ---
    **Version:** 2.0.0 Enhanced  
    **Last Updated:** December 2025
    """
)

# ---------------- UPDATE SESSION INFO ----------------
update_last_session()
check_daily_streak()

# ---------------- ROUTING ----------------
try:
    if section == "🏠 Dashboard":
        render_dashboard(nlp)
    
    elif section == "🧬 Vocabulary Intelligence":
        vocab_system = OmicsVocabularySystem()
        vocab_system.render()
    
    elif section == "📖 Interactive Reading":
        reading_comp = OmicsReadingComprehension()
        reading_comp.render()
    
    elif section == "✍️ Writing Assistant":
        render_omics_writing_assistant(nlp)
    
    elif section == "📊 Progress Analytics":
        render_progress_analytics()
    
    elif section == "🎯 Daily Challenge":
        render_daily_challenge(nlp)

except Exception as e:
    logger.error(f"Error in section {section}: {e}")
    st.error(f"An error occurred. Please try again or switch sections.")
    if st.button("🔄 Reload App"):
        st.rerun()

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#6b7280; font-size:14px;">
        <p><strong>OmicsLingua v2.0</strong> — Scientific English Learning Platform</p>
        <p>Author: Dr. MERZOUG Mohamed (ESSBO) | © 2025 Higher School of Biological Sciences of Oran</p>
        <p>🧬 Empowering bioinformatics students with scientific English proficiency</p>
    </div>
    """,
    unsafe_allow_html=True
)
