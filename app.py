import streamlit as st
import pandas as pd
import json
from utils.ui import load_css, display_term_card
from pathlib import Path

st.set_page_config(
    page_title="OmicsLingua | Scientific English Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

col1, col2 = st.columns([1, 6])
with col1:
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=200)
    else:
        st.markdown("### 🧬")
        
with col2:
    st.title("OmicsLingua")
    st.markdown("**The Reference Platform for Scientific English in Omics & Genetic Engineering**")

st.markdown("---")

@st.cache_data
def load_glossary():
    """Load glossary from JSON or CSV files."""
    # Try JSON first (in data folder)
    json_path = Path('data/omics_vocabulary.json')
    if json_path.exists():
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
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
            st.sidebar.success(f"✅ Loaded {len(df)} terms from JSON")
            return df
        except Exception as e:
            st.sidebar.error(f"❌ JSON Error: {str(e)}")
    
    # Try CSV files
    csv_files = ['batch1_institutional_glossary.csv', 'batch2_institutional_glossary.csv', 'batch3_institutional_glossary.csv']
    all_terms = []
    for file in csv_files:
        if Path(file).exists():
            try:
                df = pd.read_csv(file)
                all_terms.append(df)
                st.sidebar.success(f"✅ Loaded {file}")
            except Exception as e:
                st.sidebar.warning(f"⚠️ {file}: {str(e)}")
    
    if all_terms:
        combined = pd.concat(all_terms, ignore_index=True)
        return combined
    
    st.error("❌ No data files found! Please upload data/omics_vocabulary.json or CSV files.")
    return pd.DataFrame(columns=['term', 'definition', 'category', 'level', 'usage_example', 'synonyms'])

glossary_df = load_glossary()

st.sidebar.header("🔍 Filter Options")
search_term = st.sidebar.text_input("Search terms:", placeholder="Type to search...")

if len(glossary_df) > 0 and 'category' in glossary_df.columns:
    categories = ['All'] + sorted(glossary_df['category'].dropna().unique().tolist())
else:
    categories = ['All']
selected_category = st.sidebar.selectbox("Category:", categories)

if len(glossary_df) > 0 and 'level' in glossary_df.columns:
    levels = ['All'] + sorted(glossary_df['level'].dropna().unique().tolist())
else:
    levels = ['All']
selected_level = st.sidebar.selectbox("Difficulty Level:", levels)

filtered_df = glossary_df.copy()

if search_term and len(filtered_df) > 0:
    filtered_df = filtered_df[
        filtered_df['term'].str.contains(search_term, case=False, na=False) |
        filtered_df['definition'].str.contains(search_term, case=False, na=False)
    ]

if selected_category != 'All' and len(filtered_df) > 0:
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

if selected_level != 'All' and len(filtered_df) > 0:
    filtered_df = filtered_df[filtered_df['level'] == selected_level]

st.markdown(f"### Showing **{len(filtered_df)}** term(s)")

if len(filtered_df) > 0:
    for idx, row in filtered_df.iterrows():
        display_term_card(row.to_dict())
else:
    st.info("No terms found matching your criteria. Try adjusting your filters.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>© 2025 OmicsLingua Platform | ESSBO</p>
    <p><strong>Expert in Microbial Genomics, Bioinformatics & Scientific Education</strong></p>
</div>
""", unsafe_allow_html=True)