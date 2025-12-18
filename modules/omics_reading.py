import streamlit as st
import re

class OmicsReadingComprehension:
    """
    Interactive reading comprehension with domain-specific scientific texts.
    Developer: Dr. MERZOUG Mohamed, ESSBO
    """
    
    def __init__(self):
        self.passages = self._load_passages()
    
    def _load_passages(self):
        """Curated research passages from omics literature."""
        return {
            "Genomics & Sequencing": {
                "title": "Next-Generation Sequencing in Clinical Genomics",
                "text": """Next-generation sequencing (NGS) technologies have revolutionized clinical genomics by enabling comprehensive genomic profiling at unprecedented scale and speed. Whole-genome sequencing (WGS) and whole-exome sequencing (WES) are now routinely employed to identify pathogenic variants in patients with rare genetic disorders. The transition from Sanger sequencing to NGS platforms has reduced per-base sequencing costs by several orders of magnitude while dramatically increasing throughput. Contemporary NGS workflows typically achieve >30× coverage depth, ensuring robust variant calling with high sensitivity and specificity. However, interpretation of variants of uncertain significance (VUS) remains a significant challenge, necessitating integration of population frequency databases, in silico prediction algorithms, and functional validation studies to establish clinical pathogenicity.""",
                "glossary": {
                    "Next-generation sequencing": "High-throughput sequencing technologies that enable parallel sequencing of millions of DNA fragments",
                    "Whole-genome sequencing": "Comprehensive sequencing of an organism's complete DNA, including coding and non-coding regions",
                    "Whole-exome sequencing": "Sequencing of all protein-coding regions (exons) of the genome, representing ~1-2% of total genomic DNA",
                    "pathogenic variants": "Genetic alterations demonstrated to cause disease phenotypes",
                    "coverage depth": "The average number of sequencing reads that align to each base position in the reference genome",
                    "variants of uncertain significance": "Genetic variants for which insufficient evidence exists to classify as pathogenic or benign"
                },
                "questions": [
                    {
                        "question": "What is the primary advantage of NGS over Sanger sequencing mentioned in the passage?",
                        "options": [
                            "Higher accuracy only",
                            "Reduced cost per base and increased throughput",
                            "Simpler interpretation of results",
                            "No need for bioinformatics analysis"
                        ],
                        "correct": 1,
                        "explanation": "The passage explicitly states that NGS has 'reduced per-base sequencing costs by several orders of magnitude while dramatically increasing throughput.'"
                    },
                    {
                        "question": "According to the text, what remains a significant challenge in clinical genomics?",
                        "options": [
                            "Achieving sufficient coverage depth",
                            "Cost of sequencing",
                            "Interpretation of variants of uncertain significance",
                            "Speed of sequencing"
                        ],
                        "correct": 2,
                        "explanation": "The passage identifies 'interpretation of variants of uncertain significance (VUS)' as 'a significant challenge.'"
                    }
                ]
            },
            "CRISPR Technology": {
                "title": "Mechanisms and Applications of CRISPR-Cas Systems",
                "text": """CRISPR-Cas9 genome editing harnesses an adaptive immune system from bacteria and archaea to achieve sequence-specific DNA cleavage. The technology requires two core components: the Cas9 endonuclease and a single-guide RNA (sgRNA) that directs Cas9 to complementary genomic loci. Upon target recognition adjacent to a protospacer adjacent motif (PAM), Cas9 introduces a double-strand break (DSB), which the cell repairs via non-homologous end joining (NHEJ) or homology-directed repair (HDR). NHEJ is error-prone and typically results in small insertions or deletions (indels), enabling gene knockout. Conversely, HDR can introduce precise edits when a homologous donor template is provided. Recent innovations include base editors that enable C-to-T or A-to-G conversions without DSBs, and prime editors that allow targeted insertions, deletions, and all 12 base-to-base transversions. Off-target cleavage at sequences with partial sgRNA complementarity remains a concern, driving development of high-fidelity Cas9 variants and improved guide RNA design algorithms.""",
                "glossary": {
                    "CRISPR-Cas9": "Clustered Regularly Interspaced Short Palindromic Repeats with Cas9 nuclease - a genome editing platform",
                    "endonuclease": "An enzyme that cleaves phosphodiester bonds within a nucleic acid chain",
                    "single-guide RNA": "A synthetic RNA molecule combining crRNA and tracrRNA sequences to guide Cas9 to target DNA",
                    "protospacer adjacent motif": "A 2-6 base pair DNA sequence immediately following the target site required for Cas9 binding and cleavage",
                    "double-strand break": "Simultaneous cleavage of both DNA strands, a key intermediate in CRISPR editing",
                    "non-homologous end joining": "Error-prone DNA repair pathway that directly ligates broken DNA ends",
                    "homology-directed repair": "High-fidelity repair mechanism using a homologous DNA template",
                    "indels": "Insertions or deletions of nucleotides in a DNA sequence",
                    "base editors": "CRISPR-derived tools enabling direct base conversion without double-strand breaks",
                    "prime editors": "Advanced genome editing tools combining nickase and reverse transcriptase for precise multi-nucleotide edits"
                },
                "questions": [
                    {
                        "question": "Which DNA repair pathway is described as 'error-prone' in the context of CRISPR editing?",
                        "options": [
                            "Homology-directed repair (HDR)",
                            "Non-homologous end joining (NHEJ)",
                            "Base excision repair",
                            "Mismatch repair"
                        ],
                        "correct": 1,
                        "explanation": "The passage states 'NHEJ is error-prone and typically results in small insertions or deletions (indels).'"
                    }
                ]
            },
            "Transcriptomics": {
                "title": "RNA-Seq for Transcriptome Analysis",
                "text": """RNA sequencing (RNA-seq) has emerged as the gold standard for comprehensive transcriptome profiling, enabling quantification of transcript abundance, discovery of novel splice variants, and identification of differentially expressed genes. Unlike hybridization-based microarrays, RNA-seq provides single-nucleotide resolution and does not require prior knowledge of transcript sequences. The typical workflow involves RNA extraction, poly(A) selection or ribosomal RNA depletion, fragmentation, reverse transcription to cDNA, library preparation, and massively parallel sequencing. Computational analysis includes read alignment to a reference genome, transcript assembly, and differential expression testing using statistical frameworks such as DESeq2 or edgeR. Appropriate experimental design with adequate biological replicates (typically n≥3) is crucial to achieve sufficient statistical power. Normalization methods such as RPKM, FPKM, or TPM account for differences in sequencing depth and transcript length. Single-cell RNA-seq (scRNA-seq) extends these capabilities to individual cells, revealing cellular heterogeneity masked in bulk tissue analysis.""",
                "glossary": {
                    "RNA sequencing": "High-throughput sequencing technology for measuring the quantity and sequences of RNA molecules in a sample",
                    "transcriptome profiling": "Comprehensive analysis of all RNA transcripts expressed in a cell or tissue",
                    "splice variants": "Different mRNA products generated from the same gene through alternative splicing",
                    "differentially expressed genes": "Genes showing statistically significant differences in expression levels between experimental conditions",
                    "poly(A) selection": "Enrichment method that captures mRNA molecules via their polyadenylated 3' tails",
                    "ribosomal RNA depletion": "Removal of abundant rRNA to enrich for other RNA species",
                    "read alignment": "Computational process of mapping sequencing reads to a reference genome",
                    "biological replicates": "Independent samples from different biological individuals or experiments",
                    "RPKM/FPKM/TPM": "Normalization metrics: Reads/Fragments Per Kilobase Million or Transcripts Per Million",
                    "Single-cell RNA-seq": "RNA sequencing performed on individual cells to capture cell-to-cell expression variability"
                },
                "questions": [
                    {
                        "question": "What is a key advantage of RNA-seq over microarrays mentioned in the passage?",
                        "options": [
                            "Lower cost",
                            "Single-nucleotide resolution without prior sequence knowledge",
                            "Faster turnaround time",
                            "Simpler analysis"
                        ],
                        "correct": 1,
                        "explanation": "The passage states RNA-seq 'provides single-nucleotide resolution and does not require prior knowledge of transcript sequences.'"
                    }
                ]
            }
        }
    
    def render(self):
        """Main rendering method for reading comprehension module."""
        st.markdown("## 📖 Interactive Scientific Reading")
        st.caption("Authentic research passages with intelligent vocabulary annotation")
        
        # Passage selection
        selected_topic = st.selectbox(
            "Select Research Topic:",
            list(self.passages.keys())
        )
        
        passage_data = self.passages[selected_topic]
        
        st.markdown(f"### {passage_data['title']}")
        
        # Reading mode selection
        mode = st.radio(
            "Reading Mode:",
            ["Annotated (Hover for definitions)", "Plain Text"],
            horizontal=True
        )
        
        if mode == "Annotated (Hover for definitions)":
            annotated_text = self._annotate_passage(
                passage_data['text'],
                passage_data['glossary']
            )
            st.markdown(annotated_text, unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: justify; line-height: 1.8;'>{passage_data['text']}</div>", 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Glossary expander
        with st.expander("📚 Technical Glossary for This Passage"):
            for term, definition in passage_data['glossary'].items():
                st.markdown(f"**{term}**: {definition}")
        
        # Comprehension questions
        st.markdown("### 🧠 Comprehension Assessment")
        
        for idx, q in enumerate(passage_data['questions']):
            st.markdown(f"**Question {idx+1}:** {q['question']}")
            answer = st.radio(
                "Select your answer:",
                q['options'],
                key=f"q_{selected_topic}_{idx}"
            )
            
            if st.button(f"Check Answer {idx+1}", key=f"check_{selected_topic}_{idx}"):
                if q['options'].index(answer) == q['correct']:
                    st.success(f"✅ Correct! {q['explanation']}")
                else:
                    st.error(f"❌ Incorrect. {q['explanation']}")
    
    def _annotate_passage(self, text, glossary):
        """Highlight technical terms with hover tooltips."""
        annotated = text
        for term, definition in glossary.items():
            # Escape special regex characters
            escaped_term = re.escape(term)
            pattern = rf'\b({escaped_term})\b'
            replacement = f'<span class="highlight-term" title="{definition}">{term}</span>'
            annotated = re.sub(pattern, replacement, annotated, flags=re.IGNORECASE)
        
        return f"<div style='text-align: justify; line-height: 1.9;'>{annotated}</div>"