import streamlit as st
from support import pdf_to_text
from support import summarize_text

st.title("Smart Study Copilot")

st.header("Welcome to Smart Study Copilot!")

def modes():
    mode = st.selectbox("Mode", ["Select a mode","Summary", "Flashcard"])
    # basically the home page.
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
    ### Flashcard Mode! (Work in progress)
    '''
    if mode == "Flashcard":
        st.write("Flashcard mode selected.")
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                flashcards = generate_flashcards(text)
            st.subheader("Flashcards:")
            for card in flashcards:
                st.write(card)
    '''
    if mode == "Flashcard":
        st.write("Still under Devlopement")
                
# be able to take in user input as a pdf first and print out the text content of the pdf
st.subheader("First upload your PDF, before you can ask any questions about it.")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
st.write("OR")
text_input = st.text_area("Or enter content of the PDF directly here:", height=200)
if uploaded_file is not None:
    text = pdf_to_text(uploaded_file)
    st.write("Successfully extracted text from the PDF. You can now move on.")
    modes()

elif text_input:
    text = text_input
    st.write("Successfully received the text input. You can now move on.")
    modes()

