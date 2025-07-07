import streamlit as st
import boto3
import io
from jd_matcher import match_resume_to_jd
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract

# ----------------------------
# Configuration
# ----------------------------

BUCKET_NAME = 'resume-analyzer-madan'
POPLER_PATH = r"C:\Users\MOKKA MADANMOHAN\OneDrive\Desktop\resume analyser\Library\bin"

# ----------------------------
# Upload Resume to S3 Bucket
# ----------------------------

def upload_to_s3(file_bytes, filename):
    try:
        s3 = boto3.client('s3')
        s3.upload_fileobj(io.BytesIO(file_bytes), BUCKET_NAME, filename)
        return True
    except Exception as e:
        st.error(f" Failed to upload to S3: {e}")
        return False

# ----------------------------
# Extract Text from PDF Using OCR
# ----------------------------

def extract_text_with_ocr(file_bytes):
    try:
        images = convert_from_bytes(file_bytes, poppler_path=POPLER_PATH)
        extracted_text = ""
        for image in images:
            extracted_text += pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        st.error(f"OCR Error: {e}")
        return ""

# ----------------------------
# Page Config + Custom Background
# ----------------------------

st.set_page_config(page_title="AI Resume Analyzer with OCR and AWS", layout="centered")

#  Custom CSS for background and styling
st.markdown("""
    <style>
        body {
            background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            padding: 2rem;
            border-radius: 12px;
        }
        .big-title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        .small-desc {
            font-size: 1.1rem;
            color: #34495e;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# App Title
# ----------------------------

st.markdown("<div class='big-title'> AI Resume Analyzer with OCR and AWS</div>", unsafe_allow_html=True)
st.markdown("<div class='small-desc'>Extracts skills from scanned resumes and matches with job description</div>", unsafe_allow_html=True)

# ----------------------------
# Resume Upload & JD Input
# ----------------------------

resume_file = st.file_uploader("📎 Upload your Resume (PDF)", type=["pdf"])
jd_text = st.text_area(" Paste the Job Description Below:", height=200)

# ----------------------------
# Processing
# ----------------------------

if resume_file and jd_text:
    file_bytes = resume_file.read()
    filename = resume_file.name

    if upload_to_s3(file_bytes, filename):
        st.success(f" Resume '{filename}' uploaded to S3 bucket: {BUCKET_NAME}")

    resume_text = extract_text_with_ocr(file_bytes)

    if resume_text:
        matched_terms, success_score = match_resume_to_jd(resume_text, jd_text)
        fail_score = 100 - success_score

        st.markdown("###  Matched Keywords")
        st.write(sorted(matched_terms) if matched_terms else "No keywords matched.")

        st.markdown("###  Success Rate")
        st.success(f"{success_score}%")

        st.markdown("###  Failure Rate")
        st.error(f"{fail_score}%")

        if success_score < 100:
            jd_terms = set(jd_text.lower().split())
            resume_terms = set(resume_text.lower().split())
            missing_terms = jd_terms - resume_terms

            if missing_terms:
                st.markdown("### 💡 Terms to Include for a Better Match")
                st.info(sorted(missing_terms))
