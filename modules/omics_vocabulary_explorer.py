import streamlit as st


def render_omics_vocabulary_explorer(vocabulary: list):
    """
    Interactive Omics Vocabulary Explorer
    Author: Dr. MERZOUG Mohamed (ESSBO)

    Parameters
    ----------
    vocabulary : list of dict
        Cleaned and normalized omics vocabulary entries
    """

    st.markdown("## 📘 Omics Vocabulary Explorer")
    st.caption("Search, filter, and explore curated terminology in genomics, molecular biology, and omics sciences.")

    if not vocabulary:
        st.warning("No vocabulary entries loaded.")
        return

    # ---------- Controls ----------
    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        search_query = st.text_input(
            "🔍 Search term",
            placeholder="e.g. CRISPR, RNA-seq, Epigenetics"
        )

    with col2:
        fields = sorted({v.get("field", "Unknown") for v in vocabulary})
        selected_field = st.selectbox(
            "Field",
            ["All"] + fields
        )

    with col3:
        difficulties = ["All", "Beginner", "Intermediate", "Advanced"]
        selected_difficulty = st.selectbox(
            "Difficulty",
            difficulties
        )

    st.markdown("---")

    # ---------- Filtering ----------
    def match(entry):
        if search_query:
            q = search_query.lower()
            if q not in entry.get("term", "").lower() and \
               not any(q in s.lower() for s in entry.get("synonyms", [])):
                return False

        if selected_field != "All" and entry.get("field") != selected_field:
            return False

        if selected_difficulty != "All" and entry.get("difficulty") != selected_difficulty:
            return False

        return True

    filtered = [e for e in vocabulary if match(e)]

    # ---------- Results ----------
    st.markdown(f"### 📚 Results ({len(filtered)})")

    if not filtered:
        st.info("No matching terms found.")
        return

    for entry in filtered:
        with st.expander(entry["term"]):
            st.markdown(f"**Definition**  
            {entry.get('definition', '—')}")

            st.markdown(
                f"**Field:** {entry.get('field', '—')}  \n"
                f"**Difficulty:** {entry.get('difficulty', '—')}"
            )

            if entry.get("usage_example"):
                st.markdown("**Usage example:**")
                st.markdown(f"> {entry['usage_example']}")

            if entry.get("synonyms"):
                st.markdown("**Synonyms:** " + ", ".join(entry["synonyms"]))

            if entry.get("related_terms"):
                st.markdown("**Related terms:** " + ", ".join(entry["related_terms"]))

            if entry.get("methods"):
                st.markdown("**Associated methods:** " + ", ".join(entry["methods"]))

            if entry.get("applications"):
                st.markdown("**Applications:** " + ", ".join(entry["applications"]))

            if entry.get("references"):
                st.markdown("**References:**")
                for ref in entry["references"]:
                    if isinstance(ref, dict):
                        st.markdown(f"- {ref.get('source')}: {ref.get('url')}")
                    else:
                        st.markdown(f"- {ref}")
