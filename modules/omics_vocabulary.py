import streamlit as st
import pandas as pd
import json
from utils.ui import term_card

class OmicsVocabularySystem:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """Load vocabulary from JSON file."""
        try:
            with open('data/omics_vocabulary.json', 'r', encoding='utf-8') as f:
                self.vocabulary = json.load(f)
        except FileNotFoundError:
            st.error("❌ Vocabulary database not found. Please check data/omics_vocabulary.json")
            self.vocabulary = []
    
    def render(self):
        """Main rendering function with modern UI."""
        st.header("🧬 Omics Vocabulary Database")
        st.markdown(f"**{len(self.vocabulary)} Scientific Terms** curated from leading genomics institutions")
        
        # Filter Panel
        with st.expander("🔍 Advanced Filters", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Domain filter
                domains = sorted(list(set([term['field'] for term in self.vocabulary])))
                selected_domain = st.selectbox(
                    "Filter by Domain",
                    options=["All Domains"] + domains
                )
            
            with col2:
                # Difficulty filter
                difficulties = ["All Levels", "Beginner", "Intermediate", "Advanced"]
                selected_difficulty = st.selectbox(
                    "Filter by Difficulty",
                    options=difficulties
                )
            
            with col3:
                # Search box
                search_query = st.text_input("🔎 Search Terms", placeholder="Type to search...")
        
        # Apply filters
        filtered_terms = self.apply_filters(
            selected_domain, 
            selected_difficulty, 
            search_query
        )
        
        # Display results count
        st.markdown(f"---\n**Showing {len(filtered_terms)} term(s)**")
        
        # Display terms in a grid layout (2 columns)
        if len(filtered_terms) == 0:
            st.warning("No terms match your filters. Try adjusting your search criteria.")
        else:
            # Create 2-column layout
            cols = st.columns(2)
            for idx, term in enumerate(filtered_terms):
                with cols[idx % 2]:
                    term_card(term)
        
        # Statistics sidebar
        with st.sidebar:
            st.markdown("### 📊 Database Statistics")
            st.metric("Total Terms", len(self.vocabulary))
            st.metric("Domains Covered", len(domains))
            st.metric("Currently Displayed", len(filtered_terms))
    
    def apply_filters(self, domain, difficulty, search_query):
        """Apply user-selected filters."""
        results = self.vocabulary
        
        # Domain filter
        if domain != "All Domains":
            results = [t for t in results if t['field'] == domain]
        
        # Difficulty filter
        if difficulty != "All Levels":
            results = [t for t in results if t['difficulty'] == difficulty]
        
        # Search filter (case-insensitive, searches term and definition)
        if search_query:
            query_lower = search_query.lower()
            results = [
                t for t in results 
                if query_lower in t['term'].lower() 
                or query_lower in t['definition'].lower()
            ]
        
        return results
