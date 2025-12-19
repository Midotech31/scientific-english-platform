"""
Configuration settings for OmicsLingua
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# NLP Settings
SPACY_MODEL = "en_core_web_sm"
MAX_TEXT_LENGTH = 10000

# Learning Settings
DAILY_WORD_GOAL = 10
WEEKLY_WORD_GOAL = 50
RETENTION_DAYS = [1, 3, 7, 14, 30]  # Spaced repetition intervals

# Vocabulary Levels
DIFFICULTY_LEVELS = {
    'beginner': {'min_freq': 100, 'color': '#10B981'},
    'intermediate': {'min_freq': 50, 'color': '#F59E0B'},
    'advanced': {'min_freq': 0, 'color': '#EF4444'}
}

# Omics Categories
OMICS_CATEGORIES = [
    'Genomics',
    'Transcriptomics',
    'Proteomics',
    'Metabolomics',
    'Epigenomics',
    'Metagenomics',
    'Lipidomics',
    'Glycomics'
]

# Writing Metrics Thresholds
WRITING_QUALITY = {
    'excellent': {'flesch_reading_ease': 50, 'avg_sentence_length': 20},
    'good': {'flesch_reading_ease': 40, 'avg_sentence_length': 25},
    'needs_improvement': {'flesch_reading_ease': 30, 'avg_sentence_length': 30}
}

# UI Settings
THEME_COLOR = '#667eea'
SECONDARY_COLOR = '#764ba2'