import re

STOP_WORDS = {
    'a','an','and','are','as','at','be','but','by','for','from','has','have','if','in','into',
    'is','it','its','no','not','of','on','or','such','that','the','their','then','there','these',
    'they','this','to','was','we','will','with','you','your','should','must','can','may','could',
    'would','been','being','do','does','did','looking','required','preferred','essential','highly'
}

def clean_and_tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return {w for w in text.split() if w and w not in STOP_WORDS}

def match_resume_to_jd(resume_text, jd_text):
    resume_words = clean_and_tokenize(resume_text)
    jd_words = clean_and_tokenize(jd_text)
    matched = jd_words & resume_words
    score = int(len(matched) / len(jd_words) * 100) if jd_words else 0
    return sorted(matched), score
