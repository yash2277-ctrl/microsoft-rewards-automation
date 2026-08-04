import random
import string

class SearchTermsGenerator:
    """Generate random search terms for Microsoft Rewards searches"""
    
    def __init__(self):
        self.topics = [
            "technology", "science", "history", "geography", "sports",
            "entertainment", "music", "movies", "books", "food",
            "travel", "nature", "animals", "space", "health",
            "fitness", "art", "culture", "gaming", "education"
        ]
        
        self.modifiers = [
            "latest", "best", "top", "how to", "what is", "why",
            "when", "where", "facts about", "guide to", "tips for",
            "history of", "future of", "benefits of", "types of"
        ]
    
    def generate_search_term(self):
        """Generate a random search term"""
        choice = random.randint(1, 3)
        
        if choice == 1:
            # Modifier + topic
            return f"{random.choice(self.modifiers)} {random.choice(self.topics)}"
        elif choice == 2:
            # Two topics combined
            return f"{random.choice(self.topics)} and {random.choice(self.topics)}"
        else:
            # Random word with number
            return f"{random.choice(self.topics)} {random.randint(2020, 2026)}"
    
    def generate_random_string(self, length=8):
        """Generate random string for variety"""
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))
    
    def get_search_terms(self, count):
        """Generate a list of unique search terms"""
        terms = set()
        while len(terms) < count:
            terms.add(self.generate_search_term())
        return list(terms)
