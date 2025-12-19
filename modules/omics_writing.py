"""
Writing Assistant Module
"""

import streamlit as st
from utils.nlp_engine import analyze_text, check_passive_voice, get_readability_score

def render_omics_writing_assistant(nlp):
    """Render writing assistant interface"""
    st.header("✍️ Scientific Writing Assistant")
    st.caption("Improve your scientific writing with real-time feedback")
    
    if not nlp:
        st.error("NLP engine not available. Some features will be limited.")
        return
    
    # Tabs for different writing tasks
    tab1, tab2, tab3 = st.tabs([
        "📝 Free Writing & Analysis",
        "📄 Abstract Builder",
        "📧 Email Templates"
    ])
    
    with tab1:
        render_free_writing_mode(nlp)
    
    with tab2:
        render_abstract_builder(nlp)
    
    with tab3:
        render_email_templates()

def render_free_writing_mode(nlp):
    """Free writing with real-time analysis"""
    st.subheader("Free Writing Mode")
    st.caption("Write and get instant feedback on your scientific text")
    
    # Text input
    user_text = st.text_area(
        "Write your text here:",
        height=250,
        placeholder="Start writing your scientific content here...\n\nExample: The human microbiome consists of trillions of microorganisms..."
    )
    
    if user_text and len(user_text.strip()) > 10:
        st.markdown("---")
        
        # Analysis section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Text Analysis")
            
            # Basic metrics
            analysis = analyze_text(user_text, nlp)
            
            if analysis:
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Words", analysis['tokens'])
                col_b.metric("Sentences", analysis['sentences'])
                col_c.metric("Avg Sentence Length", f"{analysis['avg_sentence_length']:.1f}")
                
                # Readability
                st.markdown("**Readability Scores:**")
                readability = get_readability_score(user_text)
                
                if readability:
                    col1_r, col2_r = st.columns(2)
                    with col1_r:
                        st.metric("Flesch Reading Ease", readability['flesch_reading_ease'])
                        st.caption("Higher = Easier to read (aim for 50-60 for scientific)")
                    with col2_r:
                        st.metric("Grade Level", readability['flesch_kincaid_grade'])
                        st.caption("Appropriate for graduate level: 12-16")
                
                # Passive voice detection
                st.markdown("**Passive Voice Check:**")
                passive_sentences = check_passive_voice(user_text, nlp)
                
                if passive_sentences:
                    st.warning(f"Found {len(passive_sentences)} passive construction(s):")
                    for sent in passive_sentences[:3]:
                        st.text(f"• {sent}")
                    if len(passive_sentences) > 3:
                        st.caption(f"... and {len(passive_sentences) - 3} more")
                    st.info("💡 Consider using active voice for clearer scientific writing")
                else:
                    st.success("✅ No passive voice detected!")
        
        with col2:
            st.subheader("💡 Suggestions")
            
            # Generate suggestions based on analysis
            suggestions = generate_writing_suggestions(user_text, analysis, nlp)
            
            for suggestion in suggestions:
                st.info(f"• {suggestion}")
            
            # Action buttons
            st.markdown("---")
            st.download_button(
                "📥 Download Text",
                user_text,
                file_name="scientific_writing.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("👆 Start typing to see real-time analysis and feedback!")

def render_abstract_builder(nlp):
    """Guided abstract writing"""
    st.subheader("📄 Structured Abstract Builder")
    st.caption("Build your scientific abstract following IMRaD format")
    
    # Initialize session state for abstract sections
    if 'abstract_sections' not in st.session_state:
        st.session_state.abstract_sections = {
            'background': '',
            'methods': '',
            'results': '',
            'conclusion': ''
        }
    
    # Background
    st.markdown("#### 1️⃣ Background/Introduction")
    st.caption("State the research problem and significance (1-2 sentences)")
    background = st.text_area(
        "Background",
        value=st.session_state.abstract_sections['background'],
        height=100,
        key='bg_input',
        placeholder="Example: The human gut microbiome plays a crucial role in health, yet its functional characterization remains incomplete..."
    )
    st.session_state.abstract_sections['background'] = background
    
    # Methods
    st.markdown("#### 2️⃣ Methods")
    st.caption("Describe your approach briefly (1-2 sentences)")
    methods = st.text_area(
        "Methods",
        value=st.session_state.abstract_sections['methods'],
        height=100,
        key='methods_input',
        placeholder="Example: We performed shotgun metagenomic sequencing on 100 fecal samples and applied functional annotation..."
    )
    st.session_state.abstract_sections['methods'] = methods
    
    # Results
    st.markdown("#### 3️⃣ Results")
    st.caption("Present key findings (2-3 sentences)")
    results = st.text_area(
        "Results",
        value=st.session_state.abstract_sections['results'],
        height=120,
        key='results_input',
        placeholder="Example: We identified 5,000 microbial genes associated with metabolic pathways..."
    )
    st.session_state.abstract_sections['results'] = results
    
    # Conclusion
    st.markdown("#### 4️⃣ Conclusion")
    st.caption("Summarize significance and implications (1-2 sentences)")
    conclusion = st.text_area(
        "Conclusion",
        value=st.session_state.abstract_sections['conclusion'],
        height=100,
        key='conclusion_input',
        placeholder="Example: This study provides a comprehensive functional map of the human gut microbiome..."
    )
    st.session_state.abstract_sections['conclusion'] = conclusion
    
    # Compile abstract
    st.markdown("---")
    st.subheader("📋 Complete Abstract")
    
    full_abstract = compile_abstract(st.session_state.abstract_sections)
    
    if full_abstract.strip():
        st.text_area("Your Abstract", full_abstract, height=250)
        
        # Analysis
        if len(full_abstract.strip()) > 50:
            word_count = len(full_abstract.split())
            st.metric("Word Count", word_count)
            
            if word_count < 150:
                st.info("💡 Most abstracts are 150-250 words")
            elif word_count > 300:
                st.warning("⚠️ Abstract may be too long. Aim for 150-250 words")
            else:
                st.success("✅ Good length for an abstract!")
        
        # Download
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download Abstract",
                full_abstract,
                file_name="scientific_abstract.txt",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("👆 Fill in the sections above to build your abstract")

def render_email_templates():
    """Scientific email templates"""
    st.subheader("📧 Scientific Email Templates")
    st.caption("Professional templates for common academic communications")
    
    template_type = st.selectbox(
        "Choose Template Type:",
        [
            "Request for Collaboration",
            "Conference Abstract Submission",
            "Manuscript Submission Cover Letter",
            "Response to Reviewers",
            "Lab Equipment Inquiry",
            "Meeting Request with Supervisor"
        ]
    )
    
    # Load template
    template_data = get_email_template(template_type)
    
    st.markdown(f"**Subject Line:** {template_data['subject']}")
    st.markdown("---")
    
    # Show template
    st.markdown("**Email Template:**")
    st.code(template_data['body'], language='text')
    
    # Customizable version
    st.markdown("**Customize Your Email:**")
    custom_email = st.text_area(
        "Edit the template:",
        template_data['body'],
        height=300
    )
    
    # Download
    st.download_button(
        "📥 Download Email",
        custom_email,
        file_name=f"{template_type.lower().replace(' ', '_')}.txt",
        mime="text/plain"
    )

def compile_abstract(sections):
    """Compile abstract from sections"""
    parts = []
    if sections['background']:
        parts.append(sections['background'])
    if sections['methods']:
        parts.append(sections['methods'])
    if sections['results']:
        parts.append(sections['results'])
    if sections['conclusion']:
        parts.append(sections['conclusion'])
    
    return ' '.join(parts)

def generate_writing_suggestions(text, analysis, nlp):
    """Generate writing improvement suggestions"""
    suggestions = []
    
    if analysis:
        # Sentence length check
        if analysis['avg_sentence_length'] > 30:
            suggestions.append("Consider breaking down long sentences for better clarity")
        
        # Word count check
        if analysis['tokens'] < 50:
            suggestions.append("Add more detail to strengthen your argument")
        
        # Entity check
        if len(analysis['entities']) == 0:
            suggestions.append("Include specific names, locations, or technical terms")
    
    # Passive voice
    passive = check_passive_voice(text, nlp)
    if len(passive) > 2:
        suggestions.append("Reduce passive voice usage - use active voice where possible")
    
    # Readability
    readability = get_readability_score(text)
    if readability and readability['flesch_reading_ease'] < 30:
        suggestions.append("Text is quite complex - consider simplifying some sentences")
    
    if not suggestions:
        suggestions.append("Great job! Your writing is clear and well-structured")
    
    return suggestions

def get_email_template(template_type):
    """Get email template by type"""
    templates = {
        "Request for Collaboration": {
            "subject": "Collaboration Opportunity in [Research Area]",
            "body": """Dear Dr. [Name],

I hope this email finds you well. My name is [Your Name], and I am a [position] at [Institution]. I have been following your research on [topic] with great interest, particularly your recent publication on [specific paper].

I am currently working on [brief description of your research], and I believe there could be valuable synergies between our work. Specifically, I am interested in [specific aspect].

Would you be interested in discussing a potential collaboration? I would be happy to schedule a video call at your convenience to explore this further.

Thank you for considering this opportunity. I look forward to hearing from you.

Best regards,
[Your Name]
[Position]
[Institution]
[Contact Information]"""
        },
        "Conference Abstract Submission": {
            "subject": "Abstract Submission for [Conference Name]",
            "body": """Dear Conference Committee,

Please find attached my abstract submission titled "[Abstract Title]" for consideration at [Conference Name] [Year].

Abstract Details:
- Presenting Author: [Name]
- Institution: [Institution]
- Category: [Research Category]
- Preferred Presentation Type: [Oral/Poster]

The abstract summarizes our recent findings on [brief description]. We believe this work would be of significant interest to the conference attendees.

Please let me know if you require any additional information.

Thank you for your consideration.

Best regards,
[Your Name]"""
        },
        "Manuscript Submission Cover Letter": {
            "subject": "Manuscript Submission - [Manuscript Title]",
            "body": """Dear Editor,

We are pleased to submit our manuscript titled "[Manuscript Title]" for consideration for publication in [Journal Name].

This manuscript presents [brief description of main findings and significance]. The work described has not been published previously and is not under consideration elsewhere.

We believe this manuscript is particularly suitable for [Journal Name] because [reasons related to journal scope].

All authors have approved the manuscript and agree with its submission to [Journal Name].

Suggested reviewers:
1. Dr. [Name], [Institution], [Email]
2. Dr. [Name], [Institution], [Email]

Thank you for considering our work.

Sincerely,
[Your Name]
Corresponding Author"""
        },
        "Response to Reviewers": {
            "subject": "Response to Reviewers - Manuscript [ID Number]",
            "body": """Dear Editor,

We thank you and the reviewers for the thoughtful comments on our manuscript titled "[Title]" (Manuscript ID: [Number]).

We have carefully addressed all comments and believe the manuscript has been substantially improved. Below, we provide a point-by-point response to each reviewer comment.

Reviewer 1:
Comment 1: [Quote reviewer comment]
Response: [Your response]
Changes: [What you changed in the manuscript]

[Continue for all comments]

We hope the revised manuscript now meets the standards of [Journal Name] and look forward to your decision.

Sincerely,
[Your Name]"""
        },
        "Lab Equipment Inquiry": {
            "subject": "Inquiry About [Equipment Name]",
            "body": """Dear [Company/Contact Name],

I am writing to inquire about [specific equipment/product]. I am a researcher at [Institution], and we are setting up a new [type of lab/facility].

Could you please provide:
1. Technical specifications for [product]
2. Pricing information
3. Delivery timeline
4. Training and support options

Our specific requirements include:
- [Requirement 1]
- [Requirement 2]

Would it be possible to arrange a demonstration or consultation?

Thank you for your assistance.

Best regards,
[Your Name]
[Position]
[Institution]
[Contact Information]"""
        },
        "Meeting Request with Supervisor": {
            "subject": "Meeting Request - [Topic]",
            "body": """Dear Prof. [Name],

I hope you are well. I would like to request a meeting to discuss [specific topic/issue].

Specifically, I would like to:
- [Point 1]
- [Point 2]
- [Point 3]

I have prepared [documents/data/analysis] and estimate we would need approximately [duration] for the discussion.

Would you have availability in the coming week? I am flexible with timing and happy to work around your schedule.

Thank you for your time.

Best regards,
[Your Name]"""
        }
    }
    
    return templates.get(template_type, templates["Request for Collaboration"])