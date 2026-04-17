import streamlit as st
from support import pdf_to_text

st.title("Smart Study Copilot")

st.header("Welcome to Smart Study Copilot!")

# be able to take in user input as a pdf first and print out the text content of the pdf
st.subheader("Upload your PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    text = pdf_to_text(uploaded_file)
    with st.spinner("Extracting text from PDF..."):
        st.write(text)
# should be good
