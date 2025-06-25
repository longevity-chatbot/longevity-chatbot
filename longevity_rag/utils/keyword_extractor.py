import spacy

# load once
_nlp = spacy.load("en_core_web_sm")

def extract_keywords(text: str, max_keywords: int = 10) -> list[str]:
    """
    Return up to max_keywords lemmas of content words,
    filtering out stop-words and punctuation.
    """
    doc = _nlp(text)
    keywords = []
    for token in doc:
        if (
            not token.is_stop
            and not token.is_punct
            and token.pos_ in {"NOUN", "PROPN", "ADJ", "VERB"}
        ):
            keywords.append(token.lemma_.lower())
            if len(keywords) >= max_keywords:
                break
    return keywords