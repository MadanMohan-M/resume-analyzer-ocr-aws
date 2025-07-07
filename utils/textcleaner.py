import spacy
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    doc = nlp(text)
    return " ".join([token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha])
