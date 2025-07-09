import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Prompt template
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech fields like software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.

You must consider that the job market is very competitive and you should provide 
the best assistance for improving the resume. Assign the percentage match based 
on the JD and highlight missing keywords.

resume: {resume_text}
description: {job_description}

I want the response in one single string having the structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit UI
st.set_page_config(page_title="Smart ATS 🧠", layout="wide")
st.markdown("<h1 style='text-align:center;'>🚀 Smart ATS Resume Matcher</h1>", unsafe_allow_html=True)
st.caption("Get instant feedback on your resume using Google Gemini")

jd = st.text_area("📌 Paste the Job Description here")
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF)", type="pdf")

if st.button("🚀 Submit"):
    if uploaded_file and jd:
        with st.spinner("Analyzing your resume..."):
            resume_text = input_pdf_text(uploaded_file)
            final_prompt = input_prompt_template.format(resume_text=resume_text, job_description=jd)
            try:
                response = get_gemini_response(final_prompt)
                try:
                    result = json.loads(response.strip())
                    # Display parsed response vertically
                    st.success("✅ Gemini Analysis Complete")

                    st.markdown("### 🎯 JD Match")
                    st.metric(label="Match Percentage", value=result.get("JD Match", "N/A"))

                    st.markdown("### 🧩 Missing Keywords")
                    if result.get("MissingKeywords"):
                        for kw in result["MissingKeywords"]:
                            st.markdown(f"- {kw}")
                    else:
                        st.write("✅ No major keywords missing!")

                    st.markdown("### 🧑‍💼 Profile Summary")
                    st.write(result.get("Profile Summary", "Not available"))

                except json.JSONDecodeError:
                    st.warning("Couldn't parse Gemini response properly. Showing raw output.")
                    st.markdown(response.replace(",", ",\n"))

            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please upload a PDF resume and paste the job description.")

st.markdown("---")
st.markdown("<p style='text-align:center;'>Made with ❤️ by Abhishek | Powered by Gemini + Streamlit</p>", unsafe_allow_html=True)
