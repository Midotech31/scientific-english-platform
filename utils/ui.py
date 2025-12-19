import streamlit as st

def load_css():
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stCard {
            background-color: white; padding: 20px; border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px;
        }
        .highlight-term {
            background-color: #e3f2fd; color: #1565c0; padding: 2px 6px;
            border-radius: 4px; font-weight: 500;
        }
        </style>
    """, unsafe_allow_html=True)

def card(title, content, context=None):
    st.markdown(f"""
    <div class="stCard">
        <h3 style="margin-top:0;">{title}</h3>
        <p style="color:#555;">{content}</p>
        {f'<div style="margin-top:10px; font-size:14px; color:#888;"><em>{context}</em></div>' if context else ''}
    </div>
    """, unsafe_allow_html=True)