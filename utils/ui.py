import streamlit as st
from pathlib import Path

def load_css():
    """Injects custom CSS for a modern, academic aesthetic."""
    st.markdown("""
    <style>
        /* Main app container */
        .main {
            background-color: #f8f9fa;
        }
        
        /* Term cards */
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
        }
        
        .badge-molecular-biology {
            background-color: #6366f1;
            color: white;
        }
        
        .badge-beginner {
            background-color: #10b981;
            color: white;
        }
        
        .badge-genomics {
            background-color: #ec4899;
            color: white;
        }
        
        /* Definition section */
        .definition-text {
            font-size: 16px;
            line-height: 1.6;
            color: #374151;
            margin-bottom: 15px;
        }
        
        /* Usage example box */
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
        
        /* Synonyms section */
        .synonyms-text {
            background-color: #fffbeb;
            padding: 10px;
            border-radius: 6px;
            margin-top: 10px;
        }
        
        /* Header styling */
        .header-container {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 30px;
        }
        
        .logo-img {
            width: 60px;
            height: 60px;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)


def render_logo():
    """Renders the application logo if it exists."""
    logo_path = Path("assets/logo.png")
    if logo_path.exists():
        st.image(str(logo_path), width=100)
    else:
        st.markdown("### 🧬 OmicsLingua")


def card(title, content, context=None):
    """Renders a UI card with optional context."""
    st.markdown(f"""
    <div class="term-card">
        <div class="term-title">{title}</div>
        {f'<p style="color: #6b7280; font-size: 14px;">{context}</p>' if context else ''}
        <div class="definition-text">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def display_term_card(term_dict):
    """Displays a formatted term card with all information."""
    # Extract term information
    term = term_dict.get('term', 'N/A')
    definition = term_dict.get('definition', 'No definition available')
    usage = term_dict.get('usage_example', '')
    synonyms = term_dict.get('synonyms', '')
    category = term_dict.get('category', 'General')
    level = term_dict.get('level', 'Intermediate')
    
    # Create badge classes based on category
    category_class = category.lower().replace(' ', '-')
    level_class = level.lower()
    
    # Build the HTML for the term card
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
    
    # Add usage example if available
    if usage and usage.strip():
        html_content += f"""
        <div class="usage-box">
            <strong>📝 Usage Example:</strong><br/>
            "{usage}"
        </div>
        """
    
    # Add synonyms if available
    if synonyms and synonyms.strip():
        html_content += f"""
        <div class="synonyms-text">
            <strong>🔤 Also known as:</strong> {synonyms}
        </div>
        """
    
    html_content += "</div>"
    
    # Render with unsafe_allow_html=True to display HTML properly
    st.markdown(html_content, unsafe_allow_html=True)