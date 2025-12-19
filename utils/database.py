"""
Simple file-based database for user progress
"""

import json
from pathlib import Path

class UserProgressDB:
    def __init__(self, db_path="data/user_progress.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
    
    def save(self, user_id, progress):
        """Save user progress"""
        # Convert sets to lists for JSON serialization
        serializable_progress = {
            k: list(v) if isinstance(v, set) else v
            for k, v in progress.items()
        }
        
        with open(self.db_path, 'w') as f:
            json.dump({user_id: serializable_progress}, f, indent=2)
    
    def load(self, user_id):
        """Load user progress"""
        if not self.db_path.exists():
            return None
        
        with open(self.db_path, 'r') as f:
            data = json.load(f)
            user_data = data.get(user_id)
            
            if user_data:
                # Convert lists back to sets
                user_data['vocab_mastered'] = set(user_data.get('vocab_mastered', []))
                user_data['vocab_learning'] = set(user_data.get('vocab_learning', []))
                return user_data
        
        return None