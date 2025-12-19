import streamlit as st

def load_css():
    """Injects custom CSS for a modern, academic aesthetic."""
    st.markdown("""
        <style>
        /* Main Container & Typography */
        .main {
            background-color: #f8f9fa; 
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3 {
            color: #2c3e50;
            font-weight: 600;
        }
        
        /* Custom Card Component */
        .stCard {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 20px;
            border: 1px solid #e9ecef;
            transition: transform 0.2s;
        }
        .stCard:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        }

        /* Highlighted Text */
        .highlight-term {
            background-color: #e3f2fd;
            color: #1565c0;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
            cursor: help;
        }
        
        /* Button Styling */
        .stButton button {
            border-radius: 8px;
            font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

def card(title, content, context=None):
    """Renders a UI card with optional context."""
    st.markdown(f"""
    <div class="stCard">
        <h3 style="margin-top:0;">{title}</h3>
        <p style="color:#555; font-size:16px;">{content}</p>
        {f'<div style="margin-top:10px; font-size:14px; color:#888;"><em>{context}</em></div>' if context else ''}
    </div>
    """, unsafe_allow_html=True)

# --- THIS IS THE MISSING FUNCTION ---
def term_card(term_dict):
    """Compact term preview card."""
    st.markdown(f"""
    <div style="border: 2px solid #e0e0e0; padding: 15px; border-radius: 8px; 
                background: #fafafa; min-height: 180px;">
        <h4 style="color: #764ba2; margin-top: 0;">{term_dict['term']}</h4>
        <p style="font-size: 13px; color: #666;">
            {term_dict['definition'][:120]}...
        </p>
        <div style="font-size: 11px; color: #999; margin-top: 10px;">
            <strong>{term_dict['field']}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)