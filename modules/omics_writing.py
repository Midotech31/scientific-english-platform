import streamlit as st
from utils.nlp_engine import analyze_text, check_passive_voice, get_readability_score
import re

def render_omics_writing_assistant(nlp):
    """
    Advanced scientific writing analyzer for omics and genetic engineering research.
    Developer: Dr. MERZOUG Mohamed, ESSBO
    """
    
    st.markdown("## ✍️ Scientific Writing Assistant")
    st.caption("AI-powered analysis for research manuscripts, abstracts, and technical reports")
    
    # Writing templates
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
    
    # Text input
    user_text = st.text_area(
        "Enter your scientific text (abstract, methods, results):",
        height=250,
        placeholder="The cells was harvested and the RNA was extracted using standard protocols..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze Writing", type="primary")
    
    if analyze_button and user_text:
        doc = analyze_text(user_text, nlp)
        
        # === Metrics Dashboard ===
        st.markdown("### 📊 Writing Quality Metrics")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        word_count = len(user_text.split())
        sentence_count = len(list(doc.sents))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        readability = get_readability_score(user_text)
        
        metric_col1.metric("Word Count", word_count)
        metric_col2.metric("Sentences", sentence_count)
        metric_col3.metric("Avg Words/Sentence", f"{avg_sentence_length:.1f}")
        metric_col4.metric("Readability Score", f"{readability}/100")
        
        st.markdown("---")
        
        # === Analysis Sections ===
        analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4 = st.tabs([
            "🎯 Grammar & Style",
            "📐 Passive Voice",
            "🔤 Academic Vocabulary",
            "💡 Improvement Suggestions"
        ])
        
        with analysis_tab1:
            st.markdown("#### Grammar & Academic Tone Analysis")
            
            # Informal language detection
            informal_words = ["kids", "stuff", "things", "a lot of", "very", "really", "good", "bad", 
                            "can't", "won't", "don't", "get", "got", "big", "small"]
            found_informal = []
            for token in doc:
                if token.text.lower() in informal_words:
                    found_informal.append(token.text)
            
            if found_informal:
                st.error(f"⚠️ **Informal Language Detected**: {', '.join(set(found_informal))}")
                st.markdown("""
                **Recommendations:**
                - Replace 'a lot of' → 'numerous', 'substantial'
                - Replace 'get' → 'obtain', 'acquire'
                - Replace 'very' → use stronger adjectives (e.g., 'crucial' instead of 'very important')
                """)
            else:
                st.success("✅ Academic tone is appropriate")
            
            # Check for hedging language (important in scientific writing)
            hedging_words = ["may", "might", "could", "suggest", "indicate", "appear", "seem", "likely", "possible"]
            found_hedging = [token.text for token in doc if token.text.lower() in hedging_words]
            
            if found_hedging:
                st.info(f"📊 **Hedging Language Usage**: {len(found_hedging)} instance(s) — {', '.join(set(found_hedging))}")
                st.caption("Appropriate hedging conveys scientific caution and precision")
            else:
                st.warning("⚠️ Consider adding hedging language to express scientific uncertainty appropriately")
        
        with analysis_tab2:
            st.markdown("#### Passive Voice Analysis")
            passive_sentences = check_passive_voice(doc)
            
            if passive_sentences:
                st.warning(f"⚠️ **Passive voice detected in {len(passive_sentences)} sentence(s)**")
                st.markdown("While passive voice is common in Methods sections, active voice improves clarity.")
                
                for idx, sent in enumerate(passive_sentences[:5], 1):
                    with st.expander(f"Passive Sentence {idx}"):
                        st.markdown(f"*Original:* {sent}")
                        st.markdown("*Tip:* Identify the actor and place them as the subject. Example:")
                        st.markdown("- Passive: 'The cells were treated with the drug.'")
                        st.markdown("- Active: 'We treated the cells with the drug.'")
            else:
                st.success("✅ No excessive passive voice detected — writing is direct and clear")
        
        with analysis_tab3:
            st.markdown("#### Academic & Technical Vocabulary")
            
            # Extract domain-specific terms (simplified heuristic)
            omics_terms = ["genomic", "transcriptomic", "proteomic", "metabolomic", "CRISPR", 
                          "sequencing", "expression", "variant", "genome", "gene", "protein",
                          "RNA", "DNA", "mutation", "editing", "phenotype", "genotype"]
            
            found_technical = []
            for token in doc:
                if token.text.lower() in omics_terms or token.pos_ == "PROPN":
                    found_technical.append(token.text)
            
            if found_technical:
                st.success(f"✅ **{len(set(found_technical))} technical terms** detected")
                st.markdown("**Identified terminology:** " + ", ".join(set(found_technical)[:15]))
            else:
                st.info("Consider incorporating domain-specific terminology to strengthen scientific rigor")
        
        with analysis_tab4:
            st.markdown("#### AI-Powered Improvement Suggestions")
            st.info("🤖 **Enhanced Rewrite Simulation** (Connect LLM API for production)")
            
            # Rule-based improvements (placeholder for LLM integration)
            improved_text = user_text.replace("was treated", "received treatment")
            improved_text = improved_text.replace("was analyzed", "underwent analysis")
            improved_text = improved_text.replace("a lot of", "numerous")
            
            col_orig, col_improved = st.columns(2)
            with col_orig:
                st.markdown("**Original Text:**")
                st.text_area("", user_text, height=200, disabled=True, key="orig")
            
            with col_improved:
                st.markdown("**Suggested Revision:**")
                st.text_area("", improved_text, height=200, key="improved")
            
            st.caption("💡 In production, integrate OpenAI/Claude API for context-aware rewrites")

    elif analyze_button:
        st.warning("⚠️ Please enter text to analyze")