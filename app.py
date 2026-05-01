import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title='AI Resume Analyzer', layout='wide')

<<<<<<< HEAD
st.title("🚀 APP IS LIVE")
=======
# Load custom CSS
def load_css():
    st.markdown(""", unsafe_allow_html=True)
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(to right, #1e1e2f, #2a2a3d);
        color: #EAEAEA;
    }
    .sidebar {
        background-color: #2c2c3d;
        padding: 20px;
    }
    .button {
        background-color: #4caf50;
        border: none;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        margin: 4px 2px;
        cursor: pointer;
    }
    </style>
    "", unsafe_allow_html=True)

load_css()

# Sidebar Navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Choose a page:', ['Home', 'Upload', 'About'])

# Home Page
if options == 'Home':
    st.title('AI Resume Analyzer')
    st.write('Welcome to the AI Resume Analyzer! Analyze and improve your resume with AI!')

# Upload Page
elif options == 'Upload':
    st.title('Upload Your Resume')
    uploaded_file = st.file_uploader('Choose a file', type=['pdf', 'docx'])
    if uploaded_file is not None:
        # Process file
        st.success('File uploaded successfully!')

# About Page
elif options == 'About':
    st.title('About This Project')
    st.write('This application uses AI to analyze resumes and suggest improvements.')

# Professional Styling with Cards
st.markdown('---')
st.header('Resume Analysis Results')
results = [{'skill': 'Python', 'score': 90}, {'skill': 'Communication', 'score': 85}]
for result in results:
    st.card(title=result['skill'], content=f"Score: {result['score']}%", style='background-color: #3a3a4e; padding: 10px; margin: 10px; border-radius: 5px;")

# Typography
st.markdown(<style>@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');</style>, unsafe_allow_html=True)
>>>>>>> 05940d99098c26514d3248cce3bdb114e8f6ea1f
