
import streamlit as st
from utils.resume_parser import parse_resume
from utils.scorer import get_ats_score, rank_resume
from utils.grammar import grammar_check
import fitz  # PyMuPDF
import docx
import os

st.title("📄 AI Resume Reviewer")

uploaded_file = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])

if uploaded_file is not None:
    # ✅ Ensure temp folder exists
    os.makedirs("temp", exist_ok=True)

    # Save uploaded file
    file_path = f"temp/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("✅ File uploaded successfully!")


    # Parse resume
    parsed_text = parse_resume(file_path)

    # Show grammar suggestions
    grammar_suggestions = grammar_check(parsed_text)

    # Show ATS Score
    ats_score = get_ats_score(parsed_text)

    # Show Rank
    rank = rank_resume(parsed_text)

    st.subheader("🔍 Resume Review")
    st.markdown(f"**ATS Score:** {ats_score}/100")
    st.markdown(f"**Rank:** {rank}")
    st.markdown("### ✍️ Grammar Suggestions")
    for g in grammar_suggestions:
        st.markdown(f"- {g}")

    st.markdown("### 📌 Resume Content")
    st.text_area("Parsed Resume", parsed_text, height=400)
