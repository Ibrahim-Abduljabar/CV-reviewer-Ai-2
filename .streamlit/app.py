import streamlit as st
import pdfplumber
from groq import Groq
from logsnag import LogSnag

log_client = LogSnag(token=st.secrets["LOGSNAG_TOKEN"], project="cv-reviewer-ai")
log_client.track(channel="visits", event="New Visit")
st.set_page_config(
    page_title="CV Reviewer AI", 
    page_icon="🔍", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.write("### 🔍 CV Reviewer AI")
st.caption("Smart CV evaluator and career advisor for comprehensive scoring, career development insights, and bypassing ATS tracking systems.")
st.divider()

with st.container():
    st.write("#### 📥 Upload Document")
    uploaded_file = st.file_uploader("Upload your resume/CV in (PDF) format", type=["pdf"])

st.divider()

if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        text_from_pdf = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    if st.button("✨ Start Immediate Evaluation & Review", use_container_width=True):
        st.write("#### 📊 Smart Career Advisor Report")
        
        with st.spinner("⏳ Analyzing resume and drafting professional recommendations..."):
            try:
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                prompt = f"You are a recruitment expert and career advisor. Evaluate the following resume accurately, provide a score out of 100, list strengths and weaknesses, and give advice to bypass ATS systems:\n{text_from_pdf}"
                
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                evaluation_result = completion.choices[0].message.content
                
                with st.container():
                    st.success("🎉 Evaluation completed successfully! Here is your comprehensive report:")
                    st.markdown(evaluation_result)
                    st.write("---") # Soft divider for completion
                
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
