import streamlit as st

def load_css():
    """Modern CSS for academic platform."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Modern Card Design */
        .term-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            border: 1px solid #e8edf2;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .term-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.1);
            border-color: #667eea;
        }
        
        .term-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        
        .term-title {
            color: #1e293b;
            font-size: 1.35rem;
            font-weight: 700;
            margin: 0;
            line-height: 1.3;
        }
        
        /* Modern Badge System */
        .badge-container {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .badge {
            font-size: 0.7rem;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }
        
        /* Domain-specific colors */
        .badge-molecular { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .badge-genomics { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; }
        .badge-bioinformatics { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
        .badge-clinical { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; }
        .badge-epigenomics { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }
        .badge-default { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #334155; }
        
        /* Difficulty badges */
        .badge-beginner { background: #e0f2fe; color: #0369a1; border: 2px solid #0ea5e9; }
        .badge-intermediate { background: #fef3c7; color: #b45309; border: 2px solid #f59e0b; }
        .badge-advanced { background: #ffe4e6; color: #be123c; border: 2px solid #f43f5e; }
        
        .definition-text {
            color: #475569;
            line-height: 1.7;
            font-size: 0.95rem;
            margin-bottom: 16px;
        }
        
        .usage-box {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 14px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
            color: #334155;
            margin-top: 12px;
            font-style: italic;
        }
        
        .synonyms-text {
            font-size: 0.85rem;
            color: #64748b;
            margin-top: 12px;
            padding-top: 12px;
            border-top: 1px dashed #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

def term_card(term_dict):
    """Render a beautiful term card with gradient badges."""
    
    # Determine domain badge class
    field = term_dict.get('field', 'General')
    badge_class = 'badge-default'
    if 'Molecular' in field: badge_class = 'badge-molecular'
    elif 'Genom' in field: badge_class = 'badge-genomics'
    elif 'Bioinformatics' in field: badge_class = 'badge-bioinformatics'
    elif 'Clinical' in field: badge_class = 'badge-clinical'
    elif 'Epigenom' in field: badge_class = 'badge-epigenomics'
    
    # Difficulty badge
    difficulty = term_dict.get('difficulty', 'Intermediate')
    diff_class = f'badge-{difficulty.lower()}'
    
    # Synonyms
    synonyms_html = ""
    if term_dict.get('synonyms') and len(term_dict['synonyms']) > 0:
        syns = ", ".join(term_dict['synonyms'])
        synonyms_html = f'<div class="synonyms-text">💡 <strong>Also known as:</strong> {syns}</div>'
    
    html = f"""
    <div class="term-card">
        <div class="term-header">
            <h3 class="term-title">{term_dict['term']}</h3>
            <div class="badge-container">
                <span class="badge {badge_class}">{field}</span>
                <span class="badge {diff_class}">{difficulty}</span>
            </div>
        </div>
        
        <div class="definition-text">
            {term_dict['definition']}
        </div>
        
        <div class="usage-box">
            <strong>📝 Usage Example:</strong><br/>
            "{term_dict['usage_example']}"
        </div>
        
        {synonyms_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def card(title, content, context=None):
    """Backward compatibility wrapper."""
    term_dict = {
        'term': title,
        'definition': content,
        'field': 'General',
        'usage_example': context or 'No example provided.',
        'difficulty': 'Intermediate'
    }
    term_card(term_dict)