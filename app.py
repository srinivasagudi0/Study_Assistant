import streamlit as st
from support import pdf_to_text
from support import summarize_text

st.title("Smart Study Copilot")

st.header("Welcome to Smart Study Copilot!")

# be able to take in user input as a pdf first and print out the text content of the pdf
st.subheader("First upload your PDF, before you can ask any questions about it.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
st.write("OR")
text_input = st.text_input("Or enter content of the PDF directly here:")
if uploaded_file is not None:
    text = pdf_to_text(uploaded_file)
    st.write("Successfully extracted text from the PDF. You can now move on.")
    mode = st.selectbox("Mode", ["Select a mode","Summary"])
    # basically a home page.
    if mode == "Select a mode":
        st.write("Please select a mode to proceed.")
    ### SUmmary Mode!
    if mode == "Summary":
        st.write("Summary mode selected.")
        if st.button("Summarize the text"):
            with st.spinner("Summarizing the text..."):
                summary = summarize_text(text)
            st.subheader("Summary:")
            st.write(summary)

elif text_input:
    st.write("Work Under Progress: Text input functionality is not yet implemented. Please upload a PDF file to proceed.")
