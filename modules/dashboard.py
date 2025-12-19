"""
Main dashboard with overview and quick actions
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

def render_dashboard(nlp):
    """Render main dashboard"""
    
    # Welcome message
    last_session = st.session_state.user_progress.get('last_session')
    if last_session:
        time_since = datetime.now() - datetime.fromisoformat(last_session)
        hours_since = int(time_since.total_seconds() / 3600)
        
        if hours_since < 24:
            greeting = "Welcome back!"
        elif hours_since < 168:  # 1 week
            greeting = f"Good to see you again! It's been {time_since.days} days."
        else:
            greeting = f"Welcome back! You've been away for {time_since.days} days."
    else:
        greeting = "Welcome to OmicsLingua!"
    
    st.header(greeting)
    st.caption("Your personalized scientific English learning dashboard")
    
    # Streak indicator
    streak = st.session_state.user_progress.get('streak_days', 0)
    if streak > 0:
        st.success(f"🔥 {streak}-day learning streak! Keep it up!")
    
    st.divider()
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        vocab_count = len(st.session_state.user_progress['vocab_mastered'])
        st.metric(
            "Words Mastered",
            vocab_count,
            delta=f"+{st.session_state.user_progress.get('words_today', 0)} today"
        )
    
    with col2:
        reading_count = len(st.session_state.user_progress['reading_completed'])
        st.metric("Articles Read", reading_count)
    
    with col3:
        writing_count = st.session_state.user_progress['writing_sessions']
        st.metric("Writing Sessions", writing_count)
    
    with col4:
        total_time = st.session_state.user_progress.get('total_time', 0)
        hours = int(total_time / 60)
        st.metric("Study Time", f"{hours}h")
    
    st.divider()
    
    # Two-column layout
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Progress chart
        st.subheader("📈 Learning Progress")
        
        # Generate sample time series data
        progress_data = generate_progress_chart_data()
        
        if not progress_data.empty:
            fig = px.line(
                progress_data,
                x='date',
                y='cumulative_words',
                title='Vocabulary Growth',
                markers=True
            )
            fig.update_traces(line_color='#667eea', line_width=3)
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Words Learned",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start learning to see your progress!")
        
        # Recent activity
        st.subheader("📋 Recent Activity")
        activity_log = st.session_state.user_progress.get('activity_log', [])
        
        if activity_log:
            for activity in activity_log[-5:]:
                st.text(f"• {activity}")
        else:
            st.info("No recent activity. Start learning!")
    
    with col_right:
        # Today's focus
        st.subheader("🎯 Today's Focus")
        
        # Recommendations
        weak_topics = identify_weak_topics()
        
        if weak_topics:
            st.warning("**Review Recommended:**")
            for topic in weak_topics[:3]:
                st.markdown(f"- {topic}")
        else:
            st.success("Great progress! Try a new topic.")
        
        # Quick actions
        st.markdown("**Quick Actions:**")
        
        if st.button("📖 Continue Last Reading", use_container_width=True):
            st.session_state.navigation_target = "📖 Interactive Reading"
            st.rerun()
        
        if st.button("🧬 Practice Vocabulary", use_container_width=True):
            st.session_state.navigation_target = "🧬 Vocabulary Intelligence"
            st.rerun()
        
        if st.button("🎯 Daily Challenge", use_container_width=True, type="primary"):
            st.session_state.navigation_target = "🎯 Daily Challenge"
            st.rerun()
        
        st.divider()
        
        # Achievements
        st.subheader("🏆 Achievements")
        display_achievements()

def generate_progress_chart_data():
    """Generate time-series data for progress chart"""
    vocab_timeline = st.session_state.user_progress.get('vocab_timeline', [])
    
    if not vocab_timeline:
        # Generate sample data if none exists
        today = datetime.now()
        sample_data = []
        cumulative = 0
        
        for i in range(30, 0, -1):
            date = today - timedelta(days=i)
            cumulative += abs(int((i % 7) * 1.5))  # Simulated growth
            sample_data.append({
                'date': date,
                'cumulative_words': cumulative
            })
        
        return pd.DataFrame(sample_data)
    
    return pd.DataFrame(vocab_timeline)

def identify_weak_topics():
    """Identify topics that need review"""
    weak_topics = []
    
    vocab_tracking = st.session_state.user_progress.get('vocab_tracking', {})
    
    # Find terms with "hard" difficulty
    for term, data in vocab_tracking.items():
        if data.get('last_difficulty') == 'hard':
            weak_topics.append(term)
    
    return weak_topics[:5]

def display_achievements():
    """Display user achievements"""
    achievements = st.session_state.user_progress.get('achievement_unlocked', [])
    
    # Define achievement milestones
    all_achievements = [
        {'id': 'first_word', 'icon': '🌱', 'title': 'First Steps', 'desc': 'Learn your first word'},
        {'id': 'ten_words', 'icon': '📚', 'title': 'Word Collector', 'desc': 'Master 10 words'},
        {'id': 'fifty_words', 'icon': '🎓', 'title': 'Vocabulary Builder', 'desc': 'Master 50 words'},
        {'id': 'streak_7', 'icon': '🔥', 'title': 'Week Warrior', 'desc': '7-day streak'},
        {'id': 'streak_30', 'icon': '💪', 'title': 'Month Master', 'desc': '30-day streak'},
        {'id': 'first_quiz', 'icon': '✏️', 'title': 'Quiz Taker', 'desc': 'Complete first quiz'},
        {'id': 'perfect_quiz', 'icon': '🏅', 'title': 'Perfectionist', 'desc': '100% quiz score'},
    ]
    
    # Check and unlock achievements
    vocab_count = len(st.session_state.user_progress['vocab_mastered'])
    streak = st.session_state.user_progress.get('streak_days', 0)
    
    # Auto-unlock based on progress
    if vocab_count >= 1 and 'first_word' not in achievements:
        achievements.append('first_word')
    if vocab_count >= 10 and 'ten_words' not in achievements:
        achievements.append('ten_words')
    if vocab_count >= 50 and 'fifty_words' not in achievements:
        achievements.append('fifty_words')
    if streak >= 7 and 'streak_7' not in achievements:
        achievements.append('streak_7')
    if streak >= 30 and 'streak_30' not in achievements:
        achievements.append('streak_30')
    
    st.session_state.user_progress['achievement_unlocked'] = achievements
    
    # Display
    if achievements:
        for ach_id in achievements[-3:]:  # Show last 3
            ach = next((a for a in all_achievements if a['id'] == ach_id), None)
            if ach:
                st.success(f"{ach['icon']} **{ach['title']}** - {ach['desc']}")
    else:
        st.info("Complete activities to unlock achievements!")