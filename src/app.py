import streamlit as st
import requests
from pdf_generator import create_pdf

API_URL = "http://localhost:8000"
st.set_page_config(page_title="English Test Generator", page_icon="📝")

def main():
    st.title("🇬🇧 English Knowledge Test Generator")
    st.markdown("Create custom English tests for grades 1-10 in seconds.")

    # Sidebar Configuration
    st.sidebar.header("Test Configuration")
    
    grade = st.sidebar.selectbox("Select Grade", list(range(1, 11)), index=4)
    
    test_type = st.sidebar.radio(
        "Test Type",
        ("Multiple Choice", "Essay", "Combination")
    )
    
    combination_ratio = 0.7
    if test_type == "Combination":
        combination_ratio = st.sidebar.slider(
            "Multiple Choice Percentage",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            format="%f"
        )
        st.sidebar.caption(f"Ratio: {int(combination_ratio*100)}% MC / {int((1-combination_ratio)*100)}% Essay")

    duration_option = st.sidebar.selectbox(
        "Duration & Volume",
        (
            "15 minutes (20 questions)",
            "60 minutes (50 questions)",
            "90 minutes (70 questions)"
        )
    )
    
    # Parse duration to get volume
    if "15 minutes" in duration_option:
        volume = 20
    elif "60 minutes" in duration_option:
        volume = 50
    else:
        volume = 70

    # Generator Button & Logic
    if "questions" not in st.session_state:
        st.session_state.questions = []
        
    # We want to regenerate when config changes, or have a manual button.
    # A manual button is often better to avoid constant reloading.
    if st.sidebar.button("Generate Test"):
        with st.spinner("Requesting questions from API..."):
            try:
                response = requests.get(
                    f"{API_URL}/generate-test",
                    params={
                        "grade": grade,
                        "count": volume,
                        "test_type": test_type,
                        "ratio": combination_ratio
                    }
                )
                if response.status_code == 200:
                    questions = response.json()
                    # Transform API response to match local format expected by pdf_generator depending on naming
                    # My API returns 'question_text', 'answer', 'options', 'points'
                    # Local generator used 'question', 'answer', 'options', 'points'
                    # Need to map 'question_text' -> 'question' or update create_pdf to use 'question_text'
                    # Let's map it here to keep pdf_generator generic or unchanged if possible.
                    # Actually pdf_generator uses q['question']. API returns q['question_text'].
                    
                    mapped_questions = []
                    for q in questions:
                        q['question'] = q['question_text'] # Map key
                        mapped_questions.append(q)
                        
                    st.session_state.questions = mapped_questions
                else:
                    st.error(f"API Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                 st.error("Failed to connect to API. Is the backend server running?")
            
    # Display Area
    if st.session_state.questions:
        st.subheader("Test Preview")
        st.caption(f"Total Questions: {len(st.session_state.questions)}")
        
        # Determine filename
        filename = f"English_Test_Grade_{grade}.pdf"
        
        # Generate PDF Button
        # In Streamlit, we generate the binary data and put it in the download button
        # But fpdf writes to file usually. We can write to a temp file or byte stream.
        # For simplicity with the existing code, we write to a temp file or simple file, read it, then download.
        
        pdf_path = "temp_test.pdf"
        create_pdf(st.session_state.questions, pdf_path)
        
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            
        st.download_button(
            label="📄 Export to PDF",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf"
        )
        
        # Show questions
        for i, q in enumerate(st.session_state.questions, 1):
            with st.expander(f"Q{i}: {q['question']} ({q['points']} pts)"):
                if "options" in q:
                    st.write("Options:")
                    for opt in q["options"]:
                        st.write(f"- {opt}")
                    st.write(f"**Answer:** {q['answer']}")
                else:
                    st.write("(Essay Question)")

    else:
        st.info("👈 Please configure the test settings in the sidebar and click 'Generate Test'.")

if __name__ == "__main__":
    main()
