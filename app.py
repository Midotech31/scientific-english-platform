import streamlit as st
from utils.ui import load_css
from utils.nlp_engine import load_model
from modules.omics_vocabulary import OmicsVocabularySystem
from modules.omics_reading import OmicsReadingComprehension
from modules.omics_writing import render_omics_writing_assistant

# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="OmicsLingua | The Reference Platform for Scientific English",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Developed by Dr. MERZOUG Mohamed, The Higher School of Biological Sciences of Oran (ESSBO)"
    }
)

# === LOAD RESOURCES ===
load_css()
nlp = load_model()
vocab_system = OmicsVocabularySystem()
reading_module = OmicsReadingComprehension()

# === SIDEBAR NAVIGATION ===
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #667eea; margin: 0;'>🧬 OmicsLingua</h1>
        <p style='color: #888; font-size: 12px; margin: 5px 0;'>
            The Reference Platform for<br/>
            <strong>Scientific English in Omics & Genetic Engineering</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    navigation = st.radio(
        "**Navigation**",
        [
            "🧬 Omics Vocabulary",
            "📖 Research Reading",
            "✍️ Writing Assistant",
            "⚖️ Grammar Trainer",
            "📊 Learning Progress"
        ],
        index=0
    )
    
    st.markdown("---")
    
    # Developer Profile
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 15px; border-radius: 10px; color: white;'>
        <h4 style='color: white; margin: 0 0 10px 0;'>👨‍🔬 Developer</h4>
        <p style='margin: 5px 0; font-size: 14px;'><strong>Dr. MERZOUG Mohamed</strong></p>
        <p style='margin: 5px 0; font-size: 12px; opacity: 0.9;'>
            Lecturer<br/>
            The Higher School of Biological Sciences of Oran (ESSBO)
        </p>
        <p style='margin: 10px 0 0 0; font-size: 11px; opacity: 0.8;'>
            Expert in Microbial Genomics, Bioinformatics & Scientific Education
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("© 2025 OmicsLingua Platform")

# === MAIN CONTENT ROUTING ===
if navigation == "🧬 Omics Vocabulary":
    vocab_system.render()

elif navigation == "📖 Research Reading":
    reading_module.render()

elif navigation == "✍️ Writing Assistant":
    if nlp:
        render_omics_writing_assistant(nlp)
    else:
        st.error("⚠️ NLP model failed to load. Run: `python -m spacy download en_core_web_sm`")

elif navigation == "⚖️ Grammar Trainer":
    st.markdown("## ⚖️ Grammar & Academic Style Trainer")
    st.info("🚧 Under Development: Interactive quizzes on passive/active voice, hedging language, and sentence structure")

elif navigation == "📊 Learning Progress":
    st.markdown("## 📊 Learning Progress Dashboard")
    st.info("🚧 Feature Roadmap: Track mastered terms, reading comprehension scores, and writing improvements")

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 12px; padding: 20px 0;'>
    <strong>OmicsLingua</strong> — The definitive Scientific English platform for researchers in Genomics, Transcriptomics, Proteomics, Metabolomics, and Genetic Engineering<br/>
    Built with Streamlit, spaCy, and scientifically validated content<br/>
    <strong>Open Source</strong> | <strong>Academic Use</strong> | <strong>Research-Grade Content</strong>
</div>
""", unsafe_allow_html=True)