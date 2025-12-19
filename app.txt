import streamlit as st
import pandas as pd
from utils.ui import load_css, render_logo, display_term_card
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
col1, col2 = st.columns([1, 8])
with col1:
    render_logo()
with col2:
    st.title("OmicsLingua")
    st.markdown("**The Reference Platform for Scientific English in Omics & Genetic Engineering**")

st.markdown("---")

# Load glossary data
@st.cache_data
def load_glossary():
    """Load all glossary CSV files."""
    glossary_files = [
        "batch1_institutional_glossary.csv",
        "batch2_institutional_glossary.csv",
        "batch3_institutional_glossary.csv"
    ]
    
    all_terms = []
    for file in glossary_files:
        file_path = Path(file)
        if file_path.exists():
            df = pd.read_csv(file_path)
            all_terms.append(df)
    
    if all_terms:
        return pd.concat(all_terms, ignore_index=True)
    else:
        # Return empty dataframe with expected columns
        return pd.DataFrame(columns=['term', 'definition', 'category', 'level', 'usage_example', 'synonyms'])

# Load data
glossary_df = load_glossary()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")

# Search box
search_term = st.sidebar.text_input("Search terms:", placeholder="Type to search...")

# Category filter
categories = ['All'] + sorted(glossary_df['category'].unique().tolist()) if 'category' in glossary_df.columns else ['All']
selected_category = st.sidebar.selectbox("Category:", categories)

# Level filter
levels = ['All'] + sorted(glossary_df['level'].unique().tolist()) if 'level' in glossary_df.columns else ['All']
selected_level = st.sidebar.selectbox("Difficulty Level:", levels)

# Filter glossary based on selections
filtered_df = glossary_df.copy()

# Apply search filter
if search_term:
    filtered_df = filtered_df[
        filtered_df['term'].str.contains(search_term, case=False, na=False) |
        filtered_df['definition'].str.contains(search_term, case=False, na=False)
    ]

# Apply category filter
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Apply level filter
if selected_level != 'All':
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