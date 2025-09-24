try:
    from spellchecker import SpellChecker
    spell = SpellChecker()
except ImportError:
    spell = None

def correct_spelling(text):
    """Correct spelling errors in text using spell checker"""
    if not spell:
        return text
    
    words = text.split()
    corrected_words = []
    
    for word in words:
        # Skip short words and numbers
        if len(word) <= 2 or word.isdigit():
            corrected_words.append(word)
            continue
            
        clean_word = word.lower().strip('.,!?;:')
        
        # If word is misspelled, get correction
        if clean_word not in spell:
            correction = spell.correction(clean_word)
            if correction and correction != clean_word:
                corrected_words.append(correction)
            else:
                corrected_words.append(word)
        else:
            corrected_words.append(word)
    
    return " ".join(corrected_words)