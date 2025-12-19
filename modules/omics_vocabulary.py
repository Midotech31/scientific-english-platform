"""
Vocabulary Intelligence System with spaced repetition and multi-modal learning
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path
import plotly.graph_objects as go

from utils.helpers import load_vocabulary_data, calculate_next_review, add_to_learning_list
from config import OMICS_CATEGORIES, DIFFICULTY_LEVELS

class OmicsVocabularySystem:
    def __init__(self):
        self.vocab_data = load_vocabulary_data()
    
    def render(self):
        st.header("🧬 Vocabulary Intelligence System")
        st.caption("Master scientific terminology with intelligent spaced repetition")
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            difficulty = st.selectbox(
                "📊 Difficulty",
                ["All", "Beginner", "Intermediate", "Advanced"]
            )
        
        with col2:
            category = st.multiselect(
                "🔬 Omics Field",
                OMICS_CATEGORIES,
                default=[]
            )
        
        with col3:
            learning_status = st.selectbox(
                "📚 Status",
                ["All", "New", "Learning", "Review Needed", "Mastered"]
            )
        
        with col4:
            search = st.text_input("🔍 Search", placeholder="Type to search...")
        
        # Filter vocabulary
        filtered_vocab = self._filter_vocabulary(difficulty, category, learning_status, search)
        
        # Tabs for different learning modes
        tab1, tab2, tab3, tab4 = st.tabs([
            "📚 Browse & Learn",
            "🎴 Flashcards",
            "✏️ Quiz Mode",
            "🔊 Pronunciation Practice"
        ])
        
        with tab1:
            self._render_browse_mode(filtered_vocab)
        
        with tab2:
            self._render_flashcard_mode(filtered_vocab)
        
        with tab3:
            self._render_quiz_mode(filtered_vocab)
        
        with tab4:
            self._render_pronunciation_mode(filtered_vocab)
    
    def _filter_vocabulary(self, difficulty, category, status, search):
        """Filter vocabulary based on criteria"""
        df = self.vocab_data.copy()
        
        if difficulty != "All":
            df = df[df['difficulty'] == difficulty.lower()]
        
        if category:
            df = df[df['category'].isin(category)]
        
        if status != "All":
            # Filter based on user progress
            user_vocab = st.session_state.user_progress
            if status == "New":
                learned = user_vocab['vocab_mastered'].union(user_vocab['vocab_learning'])
                df = df[~df['term'].isin(learned)]
            elif status == "Learning":
                df = df[df['term'].isin(user_vocab['vocab_learning'])]
            elif status == "Mastered":
                df = df[df['term'].isin(user_vocab['vocab_mastered'])]
            elif status == "Review Needed":
                df = df[df['term'].isin(self._get_review_needed_terms())]
        
        if search:
            df = df[
                df['term'].str.contains(search, case=False) |
                df['definition'].str.contains(search, case=False)
            ]
        
        return df
    
    def _render_browse_mode(self, vocab_df):
        """Browse vocabulary with detailed information"""
        st.subheader(f"📖 {len(vocab_df)} terms found")
        
        if vocab_df.empty:
            st.info("No vocabulary matches your filters. Try adjusting them!")
            return
        
        # Display options
        view_mode = st.radio("View as:", ["Cards", "Table"], horizontal=True)
        
        if view_mode == "Cards":
            # Card view
            cols_per_row = 2
            rows = [vocab_df.iloc[i:i+cols_per_row] for i in range(0, len(vocab_df), cols_per_row)]
            
            for row_data in rows:
                cols = st.columns(cols_per_row)
                for idx, (_, term_data) in enumerate(row_data.iterrows()):
                    with cols[idx]:
                        self._render_vocab_card(term_data)
        else:
            # Table view
            display_df = vocab_df[['term', 'category', 'difficulty', 'definition']].copy()
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "term": st.column_config.TextColumn("Term", width="medium"),
                    "category": st.column_config.TextColumn("Field", width="small"),
                    "difficulty": st.column_config.TextColumn("Level", width="small"),
                    "definition": st.column_config.TextColumn("Definition", width="large")
                }
            )
    
    def _render_vocab_card(self, term_data):
        """Render individual vocabulary card"""
        term = term_data['term']
        definition = term_data['definition']
        category = term_data['category']
        difficulty = term_data['difficulty']
        example = term_data.get('example', '')
        etymology = term_data.get('etymology', '')
        
        # Check learning status
        is_mastered = term in st.session_state.user_progress['vocab_mastered']
        is_learning = term in st.session_state.user_progress['vocab_learning']
        
        # Color based on difficulty
        color = DIFFICULTY_LEVELS[difficulty]['color']
        
        # Card HTML
        status_icon = "✅" if is_mastered else ("📚" if is_learning else "🆕")
        
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, {color}20 0%, {color}40 100%);
                border-left: 4px solid {color};
                border-radius: 8px;
                padding: 1.2rem;
                margin-bottom: 1rem;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #1f2937;">{status_icon} {term}</h3>
                    <span style="
                        background: {color};
                        color: white;
                        padding: 0.25rem 0.75rem;
                        border-radius: 12px;
                        font-size: 0.75rem;
                        font-weight: 600;
                    ">{difficulty.upper()}</span>
                </div>
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0.5rem 0;">
                    <strong>{category}</strong>
                </p>
                <p style="color: #374151; margin: 0.75rem 0;">
                    <strong>Definition:</strong> {definition}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Expandable details
        with st.expander("📖 More Details"):
            if example:
                st.markdown(f"**Example:** _{example}_")
            if etymology:
                st.markdown(f"**Etymology:** {etymology}")
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not is_learning and not is_mastered:
                    if st.button("➕ Add to Learning", key=f"add_{term}"):
                        st.session_state.user_progress['vocab_learning'].add(term)
                        st.success(f"Added '{term}' to learning list!")
                        st.rerun()
            
            with col2:
                if is_learning:
                    if st.button("✅ Mark Mastered", key=f"master_{term}"):
                        st.session_state.user_progress['vocab_learning'].discard(term)
                        st.session_state.user_progress['vocab_mastered'].add(term)
                        st.balloons()
                        st.success(f"'{term}' mastered!")
                        st.rerun()
            
            with col3:
                if is_mastered:
                    st.success("✅ Mastered")
    
    def _render_flashcard_mode(self, vocab_df):
        """Interactive flashcard system with spaced repetition"""
        st.subheader("🎴 Flashcard Practice")
        
        if vocab_df.empty:
            st.info("No vocabulary available. Adjust filters or add new terms!")
            return
        
        # Initialize flashcard session
        if 'flashcard_session' not in st.session_state or st.button("🔄 New Session"):
            # Prioritize review-needed terms
            review_terms = self._get_review_needed_terms()
            priority_vocab = vocab_df[vocab_df['term'].isin(review_terms)]
            
            if not priority_vocab.empty:
                deck = priority_vocab.sample(min(20, len(priority_vocab)))
                st.info(f"📌 Session includes {len(deck)} terms due for review!")
            else:
                deck = vocab_df.sample(min(20, len(vocab_df)))
            
            st.session_state.flashcard_session = {
                'deck': deck.to_dict('records'),
                'current_idx': 0,
                'show_answer': False,
                'session_stats': {'easy': 0, 'medium': 0, 'hard': 0}
            }
        
        session = st.session_state.flashcard_session
        
        if session['current_idx'] >= len(session['deck']):
            # Session complete
            st.success("🎉 Flashcard session complete!")
            
            # Show statistics
            stats = session['session_stats']
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Easy", stats['easy'])
            col2.metric("😐 Okay", stats['medium'])
            col3.metric("❌ Difficult", stats['hard'])
            
            if st.button("Start New Session"):
                del st.session_state.flashcard_session
                st.rerun()
            return
        
        # Current card
        card = session['deck'][session['current_idx']]
        
        # Progress
        progress = (session['current_idx'] + 1) / len(session['deck'])
        st.progress(progress)
        st.caption(f"Card {session['current_idx'] + 1} of {len(session['deck'])}")
        
        # Card display
        st.markdown("---")
        
        # Front of card (Term)
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                padding: 3rem 2rem;
                text-align: center;
                color: white;
                margin: 2rem 0;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                min-height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <h1 style="margin: 0; font-size: 2.5rem;">{card['term']}</h1>
                <p style="margin-top: 1rem; opacity: 0.9;">{card['category']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Flip button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Flip Card", use_container_width=True, type="primary"):
                session['show_answer'] = not session['show_answer']
                st.rerun()
        
        # Back of card (Definition, etc.)
        if session['show_answer']:
            st.markdown(
                f"""
                <div style="
                    background: #f9fafb;
                    border: 2px solid #e5e7eb;
                    border-radius: 12px;
                    padding: 2rem;
                    margin: 2rem 0;
                ">
                    <h3 style="color: #1f2937; margin-top: 0;">Definition</h3>
                    <p style="color: #374151; font-size: 1.1rem;">{card['definition']}</p>
                    
                    <h4 style="color: #1f2937; margin-top: 1.5rem;">Example</h4>
                    <p style="color: #6b7280; font-style: italic;">{card.get('example', 'No example available')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("---")
            st.markdown("**How well did you know this?**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("❌ Difficult", use_container_width=True):
                    self._process_flashcard_response(card['term'], 'hard')
                    session['session_stats']['hard'] += 1
                    self._next_flashcard()
            
            with col2:
                if st.button("😐 Okay", use_container_width=True):
                    self._process_flashcard_response(card['term'], 'medium')
                    session['session_stats']['medium'] += 1
                    self._next_flashcard()
            
            with col3:
                if st.button("✅ Easy", use_container_width=True):
                    self._process_flashcard_response(card['term'], 'easy')
                    session['session_stats']['easy'] += 1
                    self._next_flashcard()
    
    def _render_quiz_mode(self, vocab_df):
        """Interactive quiz with multiple question types"""
        st.subheader("✏️ Vocabulary Quiz")
        
        if vocab_df.empty:
            st.info("No vocabulary available for quiz. Adjust filters!")
            return
        
        # Quiz settings
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.slider("Number of questions", 5, 20, 10)
        with col2:
            question_type = st.selectbox(
                "Question type",
                ["Mixed", "Multiple Choice", "Fill in the Blank", "True/False"]
            )
        
        if st.button("🎯 Start Quiz", type="primary"):
            # Initialize quiz
            quiz_vocab = vocab_df.sample(min(num_questions, len(vocab_df)))
            
            st.session_state.quiz_session = {
                'questions': self._generate_quiz_questions(quiz_vocab, question_type),
                'current_q': 0,
                'answers': [],
                'score': 0
            }
            st.rerun()
        
        # Quiz in progress
        if 'quiz_session' in st.session_state:
            quiz = st.session_state.quiz_session
            
            if quiz['current_q'] >= len(quiz['questions']):
                # Quiz complete
                self._show_quiz_results(quiz)
                return
            
            # Current question
            q = quiz['questions'][quiz['current_q']]
            
            st.progress((quiz['current_q'] + 1) / len(quiz['questions']))
            st.markdown(f"### Question {quiz['current_q'] + 1} of {len(quiz['questions'])}")
            
            st.markdown(f"**{q['question']}**")
            
            # Answer input based on question type
            user_answer = None
            
            if q['type'] == 'multiple_choice':
                user_answer = st.radio(
                    "Select your answer:",
                    q['options'],
                    key=f"q_{quiz['current_q']}"
                )
            
            elif q['type'] == 'fill_blank':
                user_answer = st.text_input(
                    "Your answer:",
                    key=f"q_{quiz['current_q']}"
                ).strip().lower()
            
            elif q['type'] == 'true_false':
                user_answer = st.radio(
                    "Select your answer:",
                    ["True", "False"],
                    key=f"q_{quiz['current_q']}"
                )
            
            if st.button("Submit Answer", type="primary"):
                if user_answer:
                    is_correct = self._check_answer(user_answer, q['correct_answer'])
                    
                    quiz['answers'].append({
                        'question': q['question'],
                        'user_answer': user_answer,
                        'correct_answer': q['correct_answer'],
                        'is_correct': is_correct
                    })
                    
                    if is_correct:
                        quiz['score'] += 1
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Incorrect. The answer was: {q['correct_answer']}")
                        st.info(f"💡 {q.get('explanation', '')}")
                    
                    quiz['current_q'] += 1
                    
                    # Delay before next question
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.warning("Please provide an answer!")
    
    def _render_pronunciation_mode(self, vocab_df):
        """Pronunciation practice with audio"""
        st.subheader("🔊 Pronunciation Practice")
        
        if vocab_df.empty:
            st.info("No vocabulary available. Adjust filters!")
            return
        
        st.info("🎧 **Pro Tip:** Use text-to-speech in your browser or install a pronunciation extension")
        
        # Select a term
        term_list = vocab_df['term'].tolist()
        selected_term = st.selectbox("Choose a term to practice:", term_list)
        
        if selected_term:
            term_data = vocab_df[vocab_df['term'] == selected_term].iloc[0]
            
            # Display term with phonetic
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                    border-radius: 12px;
                    padding: 2rem;
                    color: white;
                    text-align: center;
                    margin: 2rem 0;
                ">
                    <h1 style="margin: 0;">{selected_term}</h1>
                    <p style="font-size: 1.5rem; margin-top: 1rem;">
                        /{term_data.get('phonetic', 'Phonetic not available')}/
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Syllable Breakdown:**")
                st.code(term_data.get('syllables', selected_term))
            
            with col2:
                st.markdown("**Stress Pattern:**")
                st.info(term_data.get('stress', 'Primary stress on first syllable'))
            
            # Etymology helps with pronunciation
            if 'etymology' in term_data:
                st.markdown("**Origin:**")
                st.write(term_data['etymology'])
            
            # Practice
            st.markdown("---")
            st.markdown("**Practice Saying:**")
            st.write(f"_{term_data['example']}_")
            
            # Mark as practiced
            if st.button("✅ Mark as Practiced"):
                st.success("Great job practicing!")
    
    # Helper methods
    def _get_review_needed_terms(self):
        """Get terms that need review based on spaced repetition"""
        review_needed = set()
        vocab_tracking = st.session_state.user_progress.get('vocab_tracking', {})
        
        today = datetime.now().date()
        
        for term, data in vocab_tracking.items():
            if 'next_review' in data:
                next_review = datetime.fromisoformat(data['next_review']).date()
                if next_review <= today:
                    review_needed.add(term)
        
        return review_needed
    
    def _process_flashcard_response(self, term, difficulty):
        """Update spaced repetition schedule"""
        if 'vocab_tracking' not in st.session_state.user_progress:
            st.session_state.user_progress['vocab_tracking'] = {}
        
        tracking = st.session_state.user_progress['vocab_tracking']
        
        if term not in tracking:
            tracking[term] = {'reviews': 0, 'last_difficulty': difficulty}
        
        tracking[term]['reviews'] += 1
        tracking[term]['last_difficulty'] = difficulty
        tracking[term]['last_review'] = datetime.now().isoformat()
        
        # Calculate next review date
        intervals = {'easy': 7, 'medium': 3, 'hard': 1}
        next_review = datetime.now() + timedelta(days=intervals[difficulty])
        tracking[term]['next_review'] = next_review.isoformat()
        
        # Add to learning or mastered
        if tracking[term]['reviews'] >= 3 and difficulty == 'easy':
            st.session_state.user_progress['vocab_mastered'].add(term)
            st.session_state.user_progress['vocab_learning'].discard(term)
        else:
            st.session_state.user_progress['vocab_learning'].add(term)
    
    def _next_flashcard(self):
        """Move to next flashcard"""
        session = st.session_state.flashcard_session
        session['current_idx'] += 1
        session['show_answer'] = False
        st.rerun()
    
    def _generate_quiz_questions(self, vocab_df, q_type):
        """Generate quiz questions"""
        questions = []
        
        for _, term_data in vocab_df.iterrows():
            if q_type in ["Mixed", "Multiple Choice"]:
                # Multiple choice question
                correct = term_data['definition']
                wrong_options = vocab_df[vocab_df['term'] != term_data['term']].sample(3)['definition'].tolist()
                options = [correct] + wrong_options
                random.shuffle(options)
                
                questions.append({
                    'type': 'multiple_choice',
                    'question': f"What is the definition of '{term_data['term']}'?",
                    'options': options,
                    'correct_answer': correct,
                    'explanation': f"In {term_data['category']}: {term_data['definition']}"
                })
        
        return questions
    
    def _check_answer(self, user_answer, correct_answer):
        """Check if answer is correct"""
        return str(user_answer).strip().lower() == str(correct_answer).strip().lower()
    
    def _show_quiz_results(self, quiz):
        """Display quiz results"""
        score_pct = (quiz['score'] / len(quiz['questions'])) * 100
        
        st.success(f"🎉 Quiz Complete! Your score: {quiz['score']}/{len(quiz['questions'])} ({score_pct:.0f}%)")
        
        # Performance gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score_pct,
            title={'text': "Your Score"},
            delta={'reference': 70},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Review incorrect answers
        if quiz['score'] < len(quiz['questions']):
            with st.expander("📝 Review Incorrect Answers"):
                for ans in quiz['answers']:
                    if not ans['is_correct']:
                        st.markdown(f"**Q:** {ans['question']}")
                        st.markdown(f"❌ Your answer: {ans['user_answer']}")
                        st.markdown(f"✅ Correct answer: {ans['correct_answer']}")
                        st.markdown("---")
        
        # Update progress
        st.session_state.user_progress['quiz_history'] = st.session_state.user_progress.get('quiz_history', [])
        st.session_state.user_progress['quiz_history'].append({
            'date': datetime.now().isoformat(),
            'score': quiz['score'],
            'total': len(quiz['questions']),
            'percentage': score_pct
        })
        
        if st.button("Take Another Quiz"):
            del st.session_state.quiz_session
            st.rerun()