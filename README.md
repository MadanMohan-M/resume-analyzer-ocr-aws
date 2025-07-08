# 🧠 AI Resume Analyzer

A smart resume analysis tool that compares your resume to a job description and highlights keyword matches. Ideal for job seekers aiming to tailor their resumes for specific roles.

---

## 🚀 Features

- 📎 Upload your resume (PDF format)
- 📄 Paste a job description
- 🧠 Get matched keyword suggestions
- 📊 View match success and improvement insights
- ☁️ Upload resumes to AWS S3 (optional)

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – UI Framework
- **PyMuPDF** – Extract text from PDF resumes
- **Boto3** – For uploading resumes to AWS S3
- **Text Processing** – Matching logic using cleaned token sets

---

## 📁 Project Structure

resume-analyzer/
├── app.py # Main Streamlit application
├── jd_matcher.py # Job description matcher logic
├── resumeparser.py # Resume text extractor from PDF
├── requirements.txt # Python dependencies
├── packages.txt # System dependencies (like poppler-utils)
├── render.yaml # Render deployment config
└── README.md # Project documentation

⚙️ How Matching Works

1. Text is extracted from the resume (PDF).
2. JD and resume text are cleaned, tokenized, and stop words are removed.
3. Matching is done based on overlapping keywords.
4. Success rate is calculated:  
   **Success % = (Matched Terms / JD Terms) × 100**
5. Missing terms are shown as improvement tips.

☁️ Deployment on Render
Push your code to GitHub.

Create a new Web Service on Render.

Point it to your GitHub repository.

Use the included render.yaml to configure Python version and startup command.

Add the required environment variables.


🔐 Environment Variables
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_DEFAULT_REGION

PYTHON_VERSION = 3.10

# 🧠 AI Resume Analyzer

**🔴 Live App**: 👉 [https://resume-analyzer-ocr-aws.onrender.com](https://resume-analyzer-ocr-aws.onrender.com/)

