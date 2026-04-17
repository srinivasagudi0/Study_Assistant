import streamlit as st
from support import pdf_to_text

st.title("Smart Study Copilot")

st.header("Welcome to Smart Study Copilot!")

# be able to take in user input as a pdf first and print out the text content of the pdf
st.subheader("First upload your PDF, before you can ask any questions about it.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    text = pdf_to_text(uploaded_file)
    st.write("Successfully extracted text from the PDF. You can now move on.")
    mode = st.selectbox("Mode", ["Summary"])
    if mode == "Summary":
        st.write("Summary mode selected.")
        # call openai api to summarize the text and print out the summary (choose a small llm mode)
        # for now just print out the text content of the pdf to make sure the pdf to text conversion works
        st.write(text)
