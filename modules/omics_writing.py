import streamlit as st
from utils.nlp_engine import analyze_text, check_passive_voice, get_readability_score


def render_omics_writing_assistant(nlp):
    """
    Advanced scientific writing analyzer for omics and genetic engineering research.
    Author: Dr. MERZOUG Mohamed (ESSBO)
    """

    st.markdown("## ✍️ Scientific Writing Assistant")
    st.caption("AI-powered analysis for research manuscripts, abstracts, and technical reports")

    # -------------------- Writing templates --------------------
    with st.expander("📋 View Sample Abstract Templates"):
        st.markdown("""
        **Genomics Study Template:**
        > Background: [Disease/condition] affects [population]. [Gene/pathway] has been implicated...  
        > Methods: We performed whole-exome sequencing on [n] samples and identified...  
        > Results: Analysis revealed [n] pathogenic variants in [genes]. Functional validation demonstrated...  
        > Conclusions: These findings elucidate the genetic architecture of [condition] and provide...

        **CRISPR Study Template:**
        > CRISPR-Cas9 genome editing enables precise modification of [target]. We designed sgRNAs targeting...  
        > Off-target analysis using [method] confirmed high specificity. HDR efficiency reached [%]...
        """)

    # -------------------- Text input --------------------
    user_text = st.text_area(
        label="Scientific Text Input",
        height=250,
        placeholder="The cells were harvested and RNA was extracted using standard protocols..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze Writing", type="primary")

    # -------------------- Analysis --------------------
    if analyze_button and user_text.strip():
        doc = analyze_text(user_text, nlp)

        # ===== Metrics Dashboard =====
        st.markdown("### 📊 Writing Quality Metrics")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        word_count = len([t for t in doc if t.is_alpha])
        sentence_count = len(list(doc.sents))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        readability = get_readability_score(doc)

        metric_col1.metric("Word Count", word_count)
        metric_col2.metric("Sentences", sentence_count)
        metric_col3.metric("Avg Words/Sentence", f"{avg_sentence_length:.1f}")
        metric_col4.metric("Readability Score", f"{readability}/100")

        st.markdown("---")

        # ===== Analysis Tabs =====
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Grammar & Style",
            "📐 Passive Voice",
            "🔤 Academic Vocabulary",
            "💡 Improvement Suggestions"
        ])

        # ---------- Grammar & Style ----------
        with tab1:
            st.markdown("#### Grammar & Academic Tone Analysis")

            informal_words = {
                "kids", "stuff", "things", "a lot of", "very", "really",
                "good", "bad", "get", "got", "big", "small"
            }

            found_informal = {t.text for t in doc if t.text.lower() in informal_words}

            if found_informal:
                st.error(f"⚠️ Informal language detected: {', '.join(found_informal)}")
                st.markdown("""
                **Recommendations:**
                - Replace *a lot of* → *numerous*, *substantial*
                - Replace *get* → *obtain*, *acquire*
                - Avoid vague intensifiers (*very*, *really*)
                """)
            else:
                st.success("✅ Academic tone is appropriate")

            hedging_words = {
                "may", "might", "could", "suggest", "indicate",
                "appear", "seem", "likely", "possible"
            }

            found_hedging = {t.text for t in doc if t.text.lower() in hedging_words}

            if found_hedging:
                st.info(f"📊 Hedging language used ({len(found_hedging)}): {', '.join(found_hedging)}")
                st.caption("Hedging conveys scientific caution and precision.")
            else:
                st.warning("⚠️ Consider adding hedging language where appropriate.")

        # ---------- Passive Voice ----------
        with tab2:
            st.markdown("#### Passive Voice Analysis")
            passive_sentences = check_passive_voice(doc)

            if passive_sentences:
                st.warning(f"⚠️ Passive voice detected in {len(passive_sentences)} sentence(s)")
                for i, sent in enumerate(passive_sentences[:5], 1):
                    with st.expander(f"Passive Sentence {i}"):
                        st.markdown(f"*Original:* {sent}")
                        st.markdown("**Tip:** Identify the actor and make it the subject.")
            else:
                st.success("✅ No excessive passive voice detected")

        # ---------- Academic Vocabulary ----------
        with tab3:
            st.markdown("#### Academic & Technical Vocabulary")

            omics_terms = {
                "genomic", "transcriptomic", "proteomic", "metabolomic", "crispr",
                "sequencing", "expression", "variant", "genome", "gene", "protein",
                "rna", "dna", "mutation", "editing", "phenotype", "genotype"
            }

            found_technical = {
                t.text for t in doc
                if t.text.lower() in omics_terms or t.pos_ == "PROPN"
            }

            if found_technical:
                st.success(f"✅ {len(found_technical)} technical terms detected")
                st.markdown(", ".join(sorted(found_technical)[:20]))
            else:
                st.info("Consider incorporating more domain-specific terminology.")

        # ---------- Improvement Suggestions ----------
        with tab4:
            st.markdown("#### AI-Powered Improvement Suggestions")
            st.info("🤖 Rule-based rewrite simulation (LLM-ready architecture)")

            improved_text = user_text
            improved_text = improved_text.replace("was treated", "received treatment")
            improved_text = improved_text.replace("was analyzed", "underwent analysis")
            improved_text = improved_text.replace("a lot of", "numerous")

            col_orig, col_improved = st.columns(2)

            with col_orig:
                st.markdown("**Original Text**")
                st.text_area(
                    label="Original Text",
                    value=user_text,
                    height=200,
                    disabled=True,
                    key="writing_orig_text"
                )

            with col_improved:
                st.markdown("**Suggested Revision**")
                st.text_area(
                    label="Improved Text",
                    value=improved_text,
                    height=200,
                    key="writing_improved_text"
                )

            st.caption("Future versions can integrate OpenAI or Claude for semantic rewrites.")

    elif analyze_button:
        st.warning("⚠️ Please enter text to analyze.")