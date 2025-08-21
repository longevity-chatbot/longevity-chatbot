import spacy

# load once
_nlp = spacy.load("en_core_web_sm")

def create_longevity_query(question: str) -> str:
    """Create a focused PubMed query for longevity research"""
    keywords = extract_keywords(question, max_keywords=5)
    
    # Add longevity context to make search more specific
    base_terms = ["longevity", "aging", "biomarker"]
    query_parts = keywords + base_terms
    
    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in query_parts:
        if term not in seen:
            seen.add(term)
            unique_terms.append(term)
    
    return " ".join(unique_terms[:8])  # Limit to 8 terms

def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """
    Return up to max_keywords lemmas of content words,
    filtering out stop-words and punctuation.
    """
    doc = _nlp(text)
    keywords = []
    
    # Longevity-specific terms to prioritize
    longevity_terms = {
        "longevity", "lifespan", "healthspan", "aging", "ageing", "biomarker", 
        "mortality", "senescence", "telomere", "oxidative", "inflammation",
        "cardiovascular", "metabolic", "cognitive", "frailty", "sarcopenia"
    }
    
    for token in doc:
        if (
            not token.is_stop
            and not token.is_punct
            and token.pos_ in {"NOUN", "PROPN", "ADJ", "VERB"}
        ):
            lemma = token.lemma_.lower()
            # Prioritize longevity-related terms
            if lemma in longevity_terms:
                keywords.insert(0, lemma)
            else:
                keywords.append(lemma)
            if len(keywords) >= max_keywords:
                break
    return keywords