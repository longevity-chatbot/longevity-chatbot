class SessionCache:
    """
    In-memory cache for the current conversation session.

    Stores the most recent vectorstore and its associated query keywords.
    Allows reuse of the vectorstore if a new query is similar to the previous one,
    based on keyword overlap.

    Methods:
        has_vectorstore(): Returns True if a vectorstore is cached.
        set_vectorstore(vectorstore, query_keywords): Caches the vectorstore and keywords.
        is_similar_query(new_keywords, threshold=0.7): Checks if the new query is similar
            to the cached one using keyword overlap.
    """
    def __init__(self):
        self.vectorstore = None
        self.last_query_keywords = None
        
    def has_vectorstore(self):
        return self.vectorstore is not None
        
    def set_vectorstore(self, vectorstore, query_keywords):
        self.vectorstore = vectorstore
        self.last_query_keywords = query_keywords
        
    def is_similar_query(self, new_keywords, threshold=0.5):
        """Check if new query is similar to cached one"""
        if not self.last_query_keywords:
            return False
            
        # Simple keyword overlap check
        old_words = set(self.last_query_keywords.lower().split())
        new_words = set(new_keywords.lower().split())
        
        if not old_words or not new_words:
            return False
            
        # Use Jaccard similarity: intersection / union
        intersection = len(old_words.intersection(new_words))
        union = len(old_words.union(new_words))
        
        similarity = intersection / union if union > 0 else 0
        
        print(f"Cache similarity check:")
        print(f"  Old: {old_words}")
        print(f"  New: {new_words}")
        print(f"  Intersection: {old_words.intersection(new_words)}")
        print(f"  Similarity: {similarity:.2f} (threshold: {threshold})")
        print(f"  Using cache: {similarity >= threshold}")
        
        return similarity >= threshold