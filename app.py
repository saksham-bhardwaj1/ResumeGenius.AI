from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to setup PDF content
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r'C:\Program Files\poppler\poppler-24.02.0\Library\bin')
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app
st.set_page_config(page_title="ATS Resume Expert", page_icon=":rocket:")
st.title("ResumeGenius.AI 👨🏽‍💻 ")

# Job description input
st.sidebar.header("Job Description 📒")
input_text = st.sidebar.text_area("Enter Job Description", key="input")

# Resume upload
st.sidebar.header("Upload Resume 📃")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Button to analyze resume
submit1 = st.sidebar.button("Analyze Resume 🌟")

# Input prompts
input_prompt1 = """
As an experienced Technical Human Resource Manager, your task is to review the provided resume.Give the summary of provided resume 
Please share your professional evaluation on the resume and also give good suggestion for better ATS score. 
"""

input_prompt2 = """
As a skilled ATS (Applicant Tracking System) scanner with a deep understanding of any field related to the Job Description like Data Science, Full Stack, Data Engineering, Python Developer, MERN Developer, DEVOPS, and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. Give me the percentage match if the resume matches the job description. 
First, the output should come as a percentage and  final thoughts make different section for each .
"""

# Button to analyze match and missing keywords
submit2 = st.sidebar.button("Match Score and analysis📊")
input_prompt3="""
Act as a Skilled ATS (Applicant Tracking System)scanner with a deep understanding of any field related to the Job Description like Data Science, Full Stack, Data Engineering, Python Developer, MERN Developer, DEVOPS, and deep ATS functionality, 
your task is to evaluate the resume against the provided job description.and give the missing keywords and also provide suggestion related to missing keywords make different section for each missing keywords and suggestion with bold colours"""
submit3=st.sidebar.button("Missing Keywords and Suggestion")

# Display results
if submit1 or submit2 or submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        if submit1:
            response = get_gemini_response(input_prompt1, pdf_content, input_text)
        elif submit2:
            response = get_gemini_response(input_prompt2, pdf_content, input_text)
        elif submit3:
            response = get_gemini_response(input_prompt3, pdf_content, input_text)

        st.subheader("Results:")
        st.write(response)
    else:
        st.warning("Please upload the resume")

if not (submit1 or submit2 or submit3):
    image = Image.open(r"D:\57aca545fa80af785f1df9127cf971fe_HeroWhatisanATS.png")
    st.image(image, use_column_width=True)

footer = """
---

*This app is powered by Gemini Pro Vision AI. For more information, visit [Gemini Pro Vision](https://ai.google.dev/models/gemini).*
"""
st.markdown(footer)
