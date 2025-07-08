import streamlit as st
import boto3
import io
import platform
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
from jd_matcher import match_resume_to_jd, clean_and_tokenize

# ----------------------------
# AWS S3 Configuration
# ----------------------------
BUCKET_NAME = 'resume-analyzer-madan'

# ----------------------------
# Platform-specific OCR setup
# ----------------------------
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
else:
    # On Render, both tesseract-ocr and poppler-utils are installed via setup.sh
    POPPLER_PATH = None

# ----------------------------
# Upload Resume to S3
# ----------------------------
def upload_to_s3(file_bytes, filename):
    try:
        s3 = boto3.client('s3')
        s3.upload_fileobj(io.BytesIO(file_bytes), BUCKET_NAME, filename)
        return True
    except Exception as e:
        st.error(f"❌ Failed to upload to S3: {e}")
        return False

# ----------------------------
# Extract Text from PDF using OCR
# ----------------------------
def extract_text_with_ocr(file_bytes):
    try:
        images = convert_from_bytes(file_bytes, poppler_path=POPPLER_PATH) if POPPLER_PATH else convert_from_bytes(file_bytes)
        extracted_text = ""
        for img in images:
            extracted_text += pytesseract.image_to_string(img)
        return extracted_text
    except Exception as e:
        st.error(f"❌ OCR Error: {e}")
        return ""

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.markdown("""
    <style>
        .stApp { background: linear-gradient(to right, #f8f9fa, #e0eafc); }
        .title { font-size: 2.5rem; font-weight: bold; color: #2c3e50; }
        .desc { font-size: 1.1rem; color: #34495e; margin-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>📄 AI Resume Analyzer (with OCR + AWS)</div>", unsafe_allow_html=True)
st.markdown("<div class='desc'>Upload a scanned resume PDF and get matching insights against a job description.</div>", unsafe_allow_html=True)

resume_file = st.file_uploader("📎 Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("🧾 Paste the Job Description Below:", height=200)

if resume_file and jd_text:
    file_bytes = resume_file.read()
    filename = resume_file.name

    if upload_to_s3(file_bytes, filename):
        st.success(f"✅ Uploaded '{filename}' to S3 Bucket '{BUCKET_NAME}'")

    resume_text = extract_text_with_ocr(file_bytes)

    if resume_text.strip():
        matched_keywords, match_score = match_resume_to_jd(resume_text, jd_text)
        st.markdown("### ✅ Matched Keywords")
        st.write(matched_keywords or "No keywords matched.")

        st.markdown("### 📊 Match Score")
        st.success(f"{match_score}%")

        if match_score < 100:
            missing = clean_and_tokenize(jd_text) - clean_and_tokenize(resume_text)
            if missing:
                st.markdown("### 💡 Terms to Improve Match")
                st.info(sorted(missing))
    else:
        st.warning("⚠️ No text extracted from the resume. Is it a valid scanned PDF?")
