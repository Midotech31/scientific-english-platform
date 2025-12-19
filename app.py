"""
OmicsLingua — Scientific English Platform for Omics & Genetic Engineering

Author: Dr. MERZOUG Mohamed
Affiliation: Higher School of Biological Sciences of Oran (ESSBO)
Year: 2025
License: MIT
"""

import streamlit as st
from pathlib import Path

from modules.omics_vocabulary import OmicsVocabularySystem
from modules.omics_reading import OmicsReadingComprehension
from modules.omics_writing import render_omics_writing_assistant
from utils.nlp_engine import load_model
from utils.ui import load_css

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OmicsLingua | Scientific English Platform",
    page_icon="🧬",
    layout="wide"
)

load_css()

# ---------------- HEADER ----------------
logo = Path("assets/MyEnglishApp Logo.png")
if logo.exists():
    st.image(str(logo), width=400)

st.title("OmicsLingua")
st.caption("The Reference Platform for Scientific English in Omics & Genetic Engineering")
st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📚 OmicsLingua Platform")
section = st.sidebar.radio(
    "Navigate to:",
    [
        "🧬 Vocabulary Intelligence",
        "📖 Interactive Reading",
        "✍️ Writing Assistant"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Author & Maintainer**  
    Dr. MERZOUG Mohamed  
    Lecturer – ESSBO  

    *Microbial Genomics · Bioinformatics · Scientific Education*
    """
)

# ---------------- NLP MODEL ----------------
@st.cache_resource
def get_nlp():
    return load_model()

nlp = get_nlp()

# ---------------- ROUTING ----------------
if section == "🧬 Vocabulary Intelligence":
    OmicsVocabularySystem().render()

elif section == "📖 Interactive Reading":
    OmicsReadingComprehension().render()

elif section == "✍️ Writing Assistant":
    render_omics_writing_assistant(nlp)

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    """
    <div style="text-align:center; color:#6b7280; font-size:14px;">
        <p><strong>OmicsLingua</strong> — Scientific English Learning Platform</p>
        <p>Author: Dr. MERZOUG Mohamed (ESSBO)</p>
        <p>© 2025 Higher School of Biological Sciences of Oran</p>
    </div>
    """,
    unsafe_allow_html=True
)
