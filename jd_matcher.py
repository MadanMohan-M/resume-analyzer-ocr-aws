import re

#  Extended Stop Words List
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by',
    'for', 'from', 'has', 'have', 'if', 'in', 'into', 'is', 'it', 'its',
    'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then',
    'there', 'these', 'they', 'this', 'to', 'was', 'we', 'will', 'with', 'you',
    'your', 'should', 'must', 'can', 'may', 'could', 'would', 'been', 'being',
    'do', 'does', 'did', 'looking', 'required', 'required.', 'desirable',
    'preferred', 'expected', 'preferred.', 'essential', 'highly', 'applicants', 'applicant'
}

def clean_and_tokenize(text):
    # Lowercase + remove punctuation
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # remove everything except letters/numbers/spaces
    words = set(text.split())

    # Remove stop words
    return {word.strip() for word in words if word not in STOP_WORDS and word.strip()}

def match_resume_to_jd(resume_text, jd_text):
    resume_words = clean_and_tokenize(resume_text)
    jd_words = clean_and_tokenize(jd_text)

    matched_words = jd_words.intersection(resume_words)
    score = int((len(matched_words) / len(jd_words)) * 100) if jd_words else 0

    return sorted(matched_words), score
