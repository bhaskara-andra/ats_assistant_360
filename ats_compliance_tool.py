import streamlit as st
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import ChatCompletion

GEMINI_API_KEY = 'AIzaSyAETnBDnIVlekpZPKw7t9cUisqqIX93sH8'

# Initialize Streamlit UI
def main():
    st.title("ATS Compliance and Job Description Comparison")
    st.sidebar.header("Upload Files")

    # File upload
    resume_file = st.sidebar.file_uploader("Upload your Resume (PDF/TXT/DOCX):", type=["pdf", "txt", "docx"])
    job_desc_file = st.sidebar.file_uploader("Upload Job Description (PDF/TXT/DOCX):", type=["pdf", "txt", "docx"])

    if st.sidebar.button("Analyze"):
        if resume_file and job_desc_file:
            resume_text = extract_text(resume_file)
            job_desc_text = extract_text(job_desc_file)

            if resume_text and job_desc_text:
                # Analyze ATS compliance and compare texts
                ats_score, missing_keywords = check_ats_compliance(resume_text, job_desc_text)

                # Display results
                st.subheader("Analysis Results")
                st.write(f"### ATS Compliance Score: {ats_score}%")

                if missing_keywords:
                    st.write("### Missing Keywords:")
                    st.write(", ".join(missing_keywords))

                # Recommendations
                recommendations = get_recommendations(missing_keywords)
                st.subheader("Recommendations")
                for rec in recommendations:
                    st.write(f"- {rec}")

            else:
                st.error("Could not extract text from one or both files.")
        else:
            st.error("Please upload both Resume and Job Description.")

# Function to extract text from uploaded files
def extract_text(file):
    import textract

    try:
        text = textract.process(file).decode('utf-8')
        return text
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

# Function to calculate ATS compliance and missing keywords
def check_ats_compliance(resume, job_desc):
    job_keywords = extract_keywords(job_desc)
    resume_keywords = extract_keywords(resume)

    matched_keywords = set(resume_keywords).intersection(set(job_keywords))
    ats_score = int((len(matched_keywords) / len(job_keywords)) * 100)

    missing_keywords = list(set(job_keywords) - set(resume_keywords))
    return ats_score, missing_keywords

# Function to extract keywords from text
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if len(word) > 3]  # Exclude very short words

# Function to get recommendations using GenAI
def get_recommendations(missing_keywords):
    try:
        openai.api_key = "your_openai_api_key"  # Replace with your API key

        prompt = (
            "Based on the missing keywords, suggest tailored recommendations to improve the resume. "
            f"Missing keywords: {', '.join(missing_keywords)}"
        )

        response = ChatCompletion.create(
            model="gpt-4",  # Specify the Gemini or OpenAI GPT model
            messages=[
                {"role": "system", "content": "You are an expert in resume optimization for ATS systems."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message['content'].split('\n')
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

if __name__ == "__main__":
    main()
