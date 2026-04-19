import streamlit as st
import random

from support import pdf_to_text
from support import summarize_text, generate_flashcards, explain_text

st.title("Smart Study Copilot")

st.header("Welcome to Smart Study Copilot!")

def modes():
    mode = st.selectbox("Mode", ["Select a mode","Summary", "Flashcard", "Quiz", "Explain"])
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
    ### Flashcard Mode! 
    if mode == "Flashcard":
        st.write("Flashcard mode selected.")
        cards = generate_flashcards(text)
        # for ddebugging
       
        if 'i' not in st.session_state: st.session_state.i = 0

    # Display Current Card
        q, a = cards[st.session_state.i]
        st.subheader(f"Question: {q}")

        if st.button("Show Answer"):
            st.write(f"Answer: {a}")

        # Navigation
        if st.button("Next"):
            st.session_state.i = (st.session_state.i + 1) % len(cards)
            st.rerun()
    ### Quiz Mode!
    if mode == "Quiz":
        st.write("Quiz mode selected.")
        cards = generate_flashcards(text)
        if 'i' not in st.session_state: st.session_state.i = 0
        if 'score' not in st.session_state: st.session_state.score = 0
        q, a = cards[st.session_state.i]
        if 'opts_i' not in st.session_state or st.session_state.opts_i != st.session_state.i:
            distractors = [ans for _, ans in cards if ans != a]
            opts = [a] + random.sample(distractors, k=min(3, len(distractors)))
            random.shuffle(opts); st.session_state.opts, st.session_state.opts_i = opts, st.session_state.i
        st.write(f"Question: {q}")
        choice = st.radio("Choose one:", st.session_state.opts, index=None)
        if st.button("Check"):
            if choice is None: st.warning("Pick an option first.")
            else:
                ok = (choice == a)
                if ok: st.session_state.score += 1; st.success("Right!")
                else: st.error(f"Wrong. Correct answer: {a}")
        if st.button("Next Question"):
            st.session_state.i = (st.session_state.i + 1) % len(cards); st.rerun()
        st.caption(f"Score: {st.session_state.score}")
    if mode == "Explain":
        st.write("Explain mode selected.")
        # now using explain_text function to explain the text.
        with st.spinner("Generating explanation..."):
            explanation = explain_text(text)
            st.subheader("Explanation:")
            st.write(explanation)
                
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
