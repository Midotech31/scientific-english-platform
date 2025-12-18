import streamlit as st
import pandas as pd
import json
import random
from utils.ui import card, term_card

class OmicsVocabularySystem:
    """
    Scientifically-curated vocabulary system for omics and genetic engineering.
    Developer: Dr. MERZOUG Mohamed, ESSBO
    """
    
    def __init__(self, data_path='data/omics_vocabulary.json'):
        self.data_path = data_path
        self.df = self.load_vocabulary()
        self.fields = self._extract_fields()
    
    def load_vocabulary(self):
        """Load scientifically validated terminology database."""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except FileNotFoundError:
            st.error("⚠️ Critical: Omics vocabulary database not found. Check data/ directory.")
            return pd.DataFrame()
    
    def _extract_fields(self):
        """Extract hierarchical field structure."""
        if not self.df.empty:
            return sorted(self.df['field'].unique().tolist())
        return []
    
    def render(self):
        """Main rendering method for vocabulary intelligence system."""
        st.markdown("## 🧬 Omics & Genetic Engineering Terminology")
        st.caption("Scientifically validated vocabulary for researchers in genomics, transcriptomics, proteomics, metabolomics, and genome editing")
        
        # === Search & Filter Interface ===
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            search_query = st.text_input(
                "🔍 Search Scientific Terms",
                placeholder="e.g., CRISPR, transcriptome, base editing...",
                help="Search across terms, definitions, and usage examples"
            )
        
        with col2:
            field_filter = st.selectbox(
                "Filter by Discipline",
                ["All Disciplines"] + self.fields
            )
        
        with col3:
            difficulty_filter = st.selectbox(
                "Level",
                ["All", "Advanced", "Expert"]
            )
        
        st.markdown("---")
        
        # === Word of the Day ===
        if 'omics_wotd' not in st.session_state:
            st.session_state.omics_wotd = self.df.sample(1).iloc[0].to_dict()
        
        # === Query Logic ===
        if not search_query:
            # Display Word of the Day
            st.markdown("### 📌 **Term of the Day**")
            self._render_detailed_term(st.session_state.omics_wotd)
            
            # Show recent additions
            st.markdown("### 🆕 Recently Added Terms")
            recent_terms = self.df.tail(6)
            cols = st.columns(3)
            for idx, (_, row) in enumerate(recent_terms.iterrows()):
                with cols[idx % 3]:
                    self._render_term_preview(row.to_dict())
        else:
            # Search Results
            results = self._search_terms(search_query, field_filter, difficulty_filter)
            
            if results.empty:
                st.warning(f"No results found for '{search_query}'. Try broader terms or check spelling.")
            else:
                st.success(f"✅ Found {len(results)} matching term(s)")
                for _, row in results.iterrows():
                    self._render_detailed_term(row.to_dict())
                    st.markdown("---")
        
        # === Browse by Field ===
        with st.expander("📚 Browse Complete Glossary by Field"):
            selected_field = st.radio("Select Omics Domain:", self.fields, horizontal=False)
            field_terms = self.df[self.df['field'] == selected_field]
            
            st.markdown(f"**{len(field_terms)} terms in {selected_field}**")
            for _, row in field_terms.iterrows():
                st.markdown(f"**{row['term']}** — {row['definition'][:100]}...")
    
    def _search_terms(self, query, field, difficulty):
        """Advanced search with multiple filters."""
        results = self.df.copy()
        
        # Text search across multiple columns
        mask = (
            results['term'].str.contains(query, case=False, na=False) |
            results['definition'].str.contains(query, case=False, na=False) |
            results['usage_example'].str.contains(query, case=False, na=False)
        )
        results = results[mask]
        
        # Field filter
        if field != "All Disciplines":
            results = results[results['field'] == field]
        
        # Difficulty filter
        if difficulty != "All":
            results = results[results['difficulty'] == difficulty.lower()]
        
        return results
    
    def _render_detailed_term(self, term_dict):
        """Render comprehensive term information."""
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; color: white; margin-bottom: 15px;">
            <h2 style="color: white; margin: 0;">{term_dict['term']}</h2>
            <p style="opacity: 0.9; margin: 5px 0 0 0;">
                <strong>Field:</strong> {term_dict['field']} | 
                <strong>Level:</strong> {term_dict['difficulty'].title()}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📖 Definition")
            st.write(term_dict['definition'])
            
            st.markdown("#### 🔬 Usage in Research Context")
            st.info(f"*\"{term_dict['usage_example']}\"*")
            
            st.markdown("#### 🌐 Scientific Context")
            st.write(term_dict['context'])
        
        with col2:
            st.markdown("#### 🔗 Related Terms")
            for rt in term_dict['related_terms']:
                st.markdown(f"- `{rt}`")
            
            st.markdown("#### 📝 Synonyms")
            for syn in term_dict['synonyms']:
                st.markdown(f"- {syn}")
    
    def _render_term_preview(self, term_dict):
        """Compact term preview card."""
        st.markdown(f"""
        <div style="border: 2px solid #e0e0e0; padding: 15px; border-radius: 8px; 
                    background: #fafafa; min-height: 180px;">
            <h4 style="color: #764ba2; margin-top: 0;">{term_dict['term']}</h4>
            <p style="font-size: 13px; color: #666;">
                {term_dict['definition'][:120]}...
            </p>
            <div style="font-size: 11px; color: #999; margin-top: 10px;">
                <strong>{term_dict['field']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)