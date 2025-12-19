"""
Omics Vocabulary Intelligence Module
Author: Dr. MERZOUG Mohamed (ESSBO)
"""

import streamlit as st
import json
from utils.ui import term_card

class OmicsVocabularySystem:
    def __init__(self):
        self.load_data()

    def load_data(self):
        try:
            with open("data/omics_vocabulary.json", encoding="utf-8") as f:
                self.vocabulary = json.load(f)
        except FileNotFoundError:
            st.error("Vocabulary database not found.")
            self.vocabulary = []

    def render(self):
        st.header("🧬 Omics Vocabulary Intelligence")
        st.markdown(f"**{len(self.vocabulary)} curated scientific terms**")

        with st.expander("🔍 Advanced Filters", expanded=True):
            col1, col2, col3 = st.columns(3)

            domains = sorted({t["field"] for t in self.vocabulary})
            with col1:
                domain = st.selectbox("Domain", ["All"] + domains)

            with col2:
                level = st.selectbox("Difficulty", ["All", "Beginner", "Intermediate", "Advanced"])

            with col3:
                query = st.text_input("Search")

        results = self.vocabulary
        if domain != "All":
            results = [t for t in results if t["field"] == domain]
        if level != "All":
            results = [t for t in results if t["difficulty"] == level]
        if query:
            q = query.lower()
            results = [t for t in results if q in t["term"].lower() or q in t["definition"].lower()]

        st.markdown(f"### Showing {len(results)} terms")

        if not results:
            st.warning("No matching terms.")
        else:
            cols = st.columns(2)
            for i, term in enumerate(results):
                with cols[i % 2]:
                    term_card(term)