import streamlit as st
import pandas as pd
import json
import html
from pathlib import Path

st.set_page_config(
    page_title="OmicsLingua | Scientific English Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# CENTERED LARGE LOGO AT TOP
logo_path = Path("assets/logo.png")
if logo_path.exists():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(str(logo_path), use_column_width=True)

st.markdown("<h1 style='text-align: center; margin-top: -20px;'>OmicsLingua</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #666;'><strong>The Reference Platform for Scientific English in Omics & Genetic Engineering</strong></p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_glossary():
    json_path = Path('data/omics_vocabulary.json')
    if not json_path.exists():
        st.error("❌ File not found!")
        return pd.DataFrame(columns=['term', 'definition', 'category', 'level', 'usage_example', 'synonyms'])
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        terms_list = []
        for item in data:
            synonyms_str = ', '.join(item.get('synonyms', [])) if item.get('synonyms') else ''
            terms_list.append({
                'term': item.get('term', 'N/A'),
                'definition': item.get('definition', ''),
                'category': item.get('field', 'General'),
                'level': item.get('difficulty', 'Intermediate'),
                'usage_example': item.get('usage_example', ''),
                'synonyms': synonyms_str
            })
        
        df = pd.DataFrame(terms_list)
        st.sidebar.success(f"✅ Loaded {len(df)} terms")
        return df
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")
        return pd.DataFrame(columns=['term', 'definition', 'category', 'level', 'usage_example', 'synonyms'])

glossary_df = load_glossary()

st.sidebar.header("🔍 Filter Options")
search_term = st.sidebar.text_input("Search terms:", placeholder="Type to search...")

if len(glossary_df) > 0:
    categories = ['All'] + sorted(glossary_df['category'].dropna().unique().tolist())
    levels = ['All'] + sorted(glossary_df['level'].dropna().unique().tolist())
else:
    categories = levels = ['All']

selected_category = st.sidebar.selectbox("Category:", categories)
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

# DISPLAY TERMS - ESCAPE HTML PROPERLY
if len(filtered_df) > 0:
    for idx, row in filtered_df.iterrows():
        term = html.escape(str(row['term']))
        definition = html.escape(str(row['definition']))
        usage = html.escape(str(row['usage_example'])) if pd.notna(row['usage_example']) else ''
        synonyms = html.escape(str(row['synonyms'])) if pd.notna(row['synonyms']) else ''
        category = html.escape(str(row['category']))
        level = html.escape(str(row['level']))
        
        card_html = f"""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; border-left: 4px solid #4CAF50;">
            <div style="font-size: 24px; font-weight: 600; color: #2c3e50; margin-bottom: 10px;">{term}</div>
            <div style="display: flex; gap: 8px; margin-bottom: 15px;">
                <span style="padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; background-color: #6366f1; color: white;">{category}</span>
                <span style="padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; background-color: #10b981; color: white;">{level}</span>
            </div>
            <div style="font-size: 16px; line-height: 1.6; color: #374151; margin-bottom: 15px;">{definition}</div>
        """
        
        if usage and usage.strip() and usage != 'nan':
            card_html += f"""
            <div style="background-color: #f0f9ff; padding: 15px; border-radius: 8px; border-left: 3px solid #3b82f6; margin-top: 10px;">
                <strong style="color: #1e40af;">📝 Usage Example:</strong><br/>
                <em style="color: #374151;">"{usage}"</em>
            </div>
            """
        
        if synonyms and synonyms.strip() and synonyms != 'nan':
            card_html += f"""
            <div style="background-color: #fffbeb; padding: 10px; border-radius: 6px; margin-top: 10px;">
                <strong style="color: #92400e;">🔤 Also known as:</strong> <span style="color: #78350f;">{synonyms}</span>
            </div>
            """
        
        card_html += "</div>"
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("No terms found. Try adjusting your filters.")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>© 2025 OmicsLingua Platform | ESSBO</p>
    <p><strong>Expert in Microbial Genomics, Bioinformatics & Scientific Education</strong></p>
</div>
""", unsafe_allow_html=True)