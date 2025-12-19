import streamlit as st
import pandas as pd
import json
from utils.ui import load_css, display_term_card
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="OmicsLingua | Scientific English Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Header with logo
col1, col2 = st.columns([1, 6])
with col1:
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=150)
    else:
        st.markdown("### 🧬")
        
with col2:
    st.title("OmicsLingua")
    st.markdown("**The Reference Platform for Scientific English in Omics & Genetic Engineering**")

st.markdown("---")

# Load glossary data from JSON
@st.cache_data
def load_glossary():
    """Load glossary from JSON file."""
    try:
        with open('omics_vocabulary.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON to DataFrame
        terms_list = []
        for term_key, term_data in data.items():
            term_dict = {
                'term': term_data.get('term', term_key),
                'definition': term_data.get('definition', ''),
                'category': term_data.get('category', 'General'),
                'level': term_data.get('level', 'Intermediate'),
                'usage_example': term_data.get('usage_example', ''),
                'synonyms': term_data.get('synonyms', '')
            }
            terms_list.append(term_dict)
        
        df = pd.DataFrame(terms_list)
        st.sidebar.success(f"✅ Loaded {len(df)} terms from omics_vocabulary.json")
        return df
        
    except FileNotFoundError:
        st.error("❌ File 'omics_vocabulary.json' not found in repository!")
        return pd.DataFrame(columns=['term', 'definition', 'category', 'level', 'usage_example', 'synonyms'])
    except Exception as e:
        st.error(f"❌ Error loading vocabulary: {str(e)}")
        return pd.DataFrame(columns=['term', 'definition', 'category', 'level', 'usage_example', 'synonyms'])

# Load data
glossary_df = load_glossary()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Search box
search_term = st.sidebar.text_input("Search terms:", placeholder="Type to search...")

# Category filter
if len(glossary_df) > 0 and 'category' in glossary_df.columns:
    categories = ['All'] + sorted(glossary_df['category'].dropna().unique().tolist())
else:
    categories = ['All']
selected_category = st.sidebar.selectbox("Category:", categories)

# Level filter
if len(glossary_df) > 0 and 'level' in glossary_df.columns:
    levels = ['All'] + sorted(glossary_df['level'].dropna().unique().tolist())
else:
    levels = ['All']
selected_level = st.sidebar.selectbox("Difficulty Level:", levels)

# Filter glossary based on selections
filtered_df = glossary_df.copy()

# Apply search filter
if search_term and len(filtered_df) > 0:
    filtered_df = filtered_df[
        filtered_df['term'].str.contains(search_term, case=False, na=False) |
        filtered_df['definition'].str.contains(search_term, case=False, na=False)
    ]

# Apply category filter
if selected_category != 'All' and len(filtered_df) > 0:
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Apply level filter
if selected_level != 'All' and len(filtered_df) > 0:
    filtered_df = filtered_df[filtered_df['level'] == selected_level]

# Display results
st.markdown(f"### Showing **{len(filtered_df)}** term(s)")

# Display terms
if len(filtered_df) > 0:
    for idx, row in filtered_df.iterrows():
        display_term_card(row.to_dict())
else:
    st.info("No terms found matching your criteria. Try adjusting your filters.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>© 2025 OmicsLingua Platform | ESSBO</p>
    <p><strong>Expert in Microbial Genomics, Bioinformatics & Scientific Education</strong></p>
</div>
""", unsafe_allow_html=True)