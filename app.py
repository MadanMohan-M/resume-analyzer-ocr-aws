import streamlit as st
import boto3
import io
import platform
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
from jd_matcher import match_resume_to_jd, clean_and_tokenize

BUCKET_NAME = 'resume-analyzer-madan'

# Detect OS for Poppler path
if platform.system() == "Windows":
    POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"
else:
    POPPLER_PATH = None  # On Render, it's in PATH

def upload_to_s3(file_bytes, filename):
    try:
        s3 = boto3.client('s3')
        s3.upload_fileobj(io.BytesIO(file_bytes), BUCKET_NAME, filename)
        return True
    except Exception as e:
        st.error(f"❌ Failed to upload to S3: {e}")
        return False

def extract_text_with_ocr(file_bytes):
    try:
        images = convert_from_bytes(file_bytes, poppler_path=POPPLER_PATH) if POPPLER_PATH else convert_from_bytes(file_bytes)
        extracted_text = "".join([pytesseract.image_to_string(img) for img in images])
        return extracted_text
    except Exception as e:
        st.error(f"❌ OCR Error: {e}")
        return ""

st.set_page_config(page_title="AI Resume Analyzer with OCR and AWS", layout="centered")

st.markdown("<h1 style='text-align: center;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Extracts skills from scanned resumes and matches with job descriptions.</p>", unsafe_allow_html=True)

resume_file = st.file_uploader("📎 Upload your Resume (PDF)", type=["pdf"])
jd_text = st.text_area("📄 Paste the Job Description Below:", height=200)

if resume_file and jd_text:
    file_bytes = resume_file.read()
    filename = resume_file.name

    if upload_to_s3(file_bytes, filename):
        st.success(f"✅ Resume '{filename}' uploaded to S3 bucket: {BUCKET_NAME}")

    resume_text = extract_text_with_ocr(file_bytes)

    if resume_text.strip():
        matched_terms, success_score = match_resume_to_jd(resume_text, jd_text)
        st.markdown("### ✅ Matched Keywords")
        st.write(sorted(matched_terms) or "No keywords matched.")

        st.markdown("### 📊 Success Rate")
        st.success(f"{success_score}%")

        st.markdown("### ❌ Failure Rate")
        st.error(f"{100 - success_score}%")

        if success_score < 100:
            jd_terms = clean_and_tokenize(jd_text)
            resume_terms = clean_and_tokenize(resume_text)
            missing_terms = jd_terms - resume_terms
            if missing_terms:
                st.markdown("### 💡 Terms to Include")
                st.info(sorted(missing_terms))
    else:
        st.warning("⚠️ No text extracted from the resume. Is it a valid scanned PDF?")
