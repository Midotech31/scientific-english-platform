"""
UI utilities and custom CSS
"""

import streamlit as st
from datetime import datetime

def load_css():
    """Load custom CSS"""
    st.markdown("""
    <style>
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        h1 { font-size: 1.5rem; }
    }
    
    /* Accessibility */
    button:focus {
        outline: 2px solid #FF4B4B;
        outline-offset: 2px;
    }
    
    /* Custom card styling */
    .vocab-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Smooth animations */
    .element-container {
        transition: all 0.3s ease;
    }
    
    /* Better readability */
    .stMarkdown {
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_profile():
    """Render user profile in sidebar"""
    with st.sidebar.expander("👤 Your Learning Profile", expanded=False):
        col1, col2 = st.columns(2)
        
        progress = st.session_state.user_progress
        
        with col1:
            st.metric("Words", len(progress['vocab_mastered']))
            st.metric("Articles", len(progress['reading_completed']))
        
        with col2:
            st.metric("Streak", f"{progress['streak_days']} days")
            st.metric("Sessions", progress['writing_sessions'])
        
        # Weekly goal
        weekly_goal = 50
        current_week = len(progress['vocab_mastered'])
        progress_pct = min(current_week / weekly_goal, 1.0)
        
        st.progress(progress_pct)
        st.caption(f"Weekly goal: {current_week}/{weekly_goal} words")