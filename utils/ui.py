import streamlit as st
from pathlib import Path

def load_css():
    """Injects custom CSS for a modern, academic aesthetic."""
    st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        
        .term-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            border-left: 4px solid #4CAF50;
        }
        
        .term-title {
            font-size: 24px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .term-badges {
            display: flex;
            gap: 8px;
            margin-bottom: 15px;
        }
        
        .badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            color: white;
        }
        
        .badge-molecular-biology { background-color: #6366f1; }
        .badge-genomics { background-color: #ec4899; }
        .badge-epigenomics { background-color: #8b5cf6; }
        .badge-transcriptomics { background-color: #f59e0b; }
        .badge-proteomics { background-color: #10b981; }
        .badge-clinical-genomics { background-color: #ef4444; }
        .badge-genetic-engineering { background-color: #06b6d4; }
        .badge-bioinformatics { background-color: #3b82f6; }
        .badge-statistics { background-color: #84cc16; }
        
        .badge-beginner { background-color: #10b981; }
        .badge-intermediate { background-color: #f59e0b; }
        .badge-advanced { background-color: #ef4444; }
        
        .definition-text {
            font-size: 16px;
            line-height: 1.6;
            color: #374151;
            margin-bottom: 15px;
        }
        
        .usage-box {
            background-color: #f0f9ff;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #3b82f6;
            margin-top: 10px;
        }
        
        .usage-box strong {
            color: #1e40af;
        }
        
        .synonyms-text {
            background-color: #fffbeb;
            padding: 10px;
            border-radius: 6px;
            margin-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)


def display_term_card(term_dict):
    """Displays a formatted term card with all information."""
    term = term_dict.get('term', 'N/A')
    definition = term_dict.get('definition', 'No definition available')
    usage = term_dict.get('usage_example', '')
    synonyms = term_dict.get('synonyms', '')
    category = term_dict.get('category', 'General')
    level = term_dict.get('level', 'Intermediate')
    
    # Create safe CSS class names
    category_class = category.lower().replace(' ', '-').replace('/', '-')
    level_class = level.lower()
    
    html_content = f"""
    <div class="term-card">
        <div class="term-title">{term}</div>
        <div class="term-badges">
            <span class="badge badge-{category_class}">{category}</span>
            <span class="badge badge-{level_class}">{level}</span>
        </div>
        <div class="definition-text">
            {definition}
        </div>
    """
    
    if usage and usage.strip():
        html_content += f"""
        <div class="usage-box">
            <strong>📝 Usage Example:</strong><br/>
            "{usage}"
        </div>
        """
    
    if synonyms and synonyms.strip():
        html_content += f"""
        <div class="synonyms-text">
            <strong>🔤 Also known as:</strong> {synonyms}
        </div>
        """
    
    html_content += "</div>"
    
    # THIS IS THE KEY: unsafe_allow_html=True
    st.markdown(html_content, unsafe_allow_html=True)