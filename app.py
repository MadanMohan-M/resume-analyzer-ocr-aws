import streamlit as st
import boto3
import io
import fitz  # PyMuPDF
from jd_matcher import match_resume_to_jd, clean_and_tokenize

BUCKET = 'resume-analyzer-madan'

def upload_to_s3(bytes_data, fname):
    try:
        boto3.client('s3').upload_fileobj(io.BytesIO(bytes_data), BUCKET, fname)
        return True
    except Exception as e:
        st.error(f"S3 Upload Error: {e}")
        return False

def extract_text_from_pdf_bytes(b):
    doc = fitz.open(stream=b, filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

st.set_page_config(page_title="Resume Analyzer (No OCR)", layout="centered")
st.title("📄 Resume Analyzer (No OCR) with AWS S3")

resume = st.file_uploader("Upload PDF Resume", type=["pdf"])
jd = st.text_area("Paste Job Description", height=200)

if resume and jd:
    data = resume.read()
    if upload_to_s3(data, resume.name):
        st.success(f"✅ Uploaded {resume.name} to S3")

    text = extract_text_from_pdf_bytes(data)
    matched, score = match_resume_to_jd(text, jd)
    st.subheader("Matched Keywords")
    st.write(matched or "None")

    st.subheader("✅ Success Rate")
    st.success(f"{score}%")

    st.subheader("❌ Failure Rate")
    st.error(f"{100 - score}%")

    if score < 100:
        jd_set = clean_and_tokenize(jd)
        resume_set = clean_and_tokenize(text)
        missing = sorted(jd_set - resume_set)
        st.subheader("💡 Terms to Include")
        st.write(missing)
