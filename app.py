import streamlit as st
import random
import auth
from support import pdf_to_text, trick_questions
from support import summarize_text, generate_flashcards, explain_text, chat_with_assistant

st.title("Smart Study Copilot")

st.header("Welcome to Smart Study Copilot!")

def require_login() -> None:
    auth.ensure_default_admin()  # defaults to admin/admin (override via env)

    st.session_state.setdefault("authed", False)
    st.session_state.setdefault("user", "")
    # Clear widget state on next run (Streamlit forbids modifying widget keys after creation)
    for key in st.session_state.pop("_clear_keys", []):
        st.session_state[key] = ""

    if st.session_state.authed:
        with st.sidebar:
            st.caption(f"Signed in as: {st.session_state.user or 'user'}")
            with st.expander("Change password"):
                old = st.text_input("Current password", type="password", key="pw_old")
                new = st.text_input("New password", type="password", key="pw_new")
                if st.button("Change password"):
                    if auth.change_password(st.session_state.user, old, new):
                        st.success("Password updated.")
                        st.session_state["_clear_keys"] = ["pw_old", "pw_new"]
                        st.rerun()
                    else:
                        st.error("Couldn’t update password. Check your current password.")
            if st.button("Logout"):
                st.session_state.authed = False
                st.session_state.user = ""
                st.rerun()
        return

    st.subheader("Welcome back")
    tab_login, tab_create = st.tabs(["Sign in", "Create account"])

    with tab_login:
        username = st.text_input("Username", placeholder="admin", key="login_user")
        password = st.text_input("Password", type="password", key="login_pw")
        st.caption("Default login is admin / admin")
        if st.button("Login", use_container_width=True):
            if auth.authenticate(username, password):
                st.session_state.authed = True
                st.session_state.user = username.strip()
                st.session_state["_clear_keys"] = ["login_pw"]
                st.success("Signed in.")
                st.rerun()
            else:
                st.error("That username/password didn’t match.")

    with tab_create:
        new_u = st.text_input("New username", key="create_user")
        new_p = st.text_input("New password", type="password", key="create_pw")
        if st.button("Create account", use_container_width=True):
            try:
                auth.create_user(new_u, new_p)
                st.success("Account created. You can sign in now.")
                st.session_state["_clear_keys"] = ["create_pw"]
                st.rerun()
            except ValueError:
                st.error("Enter a username and password.")
            except Exception:
                st.error("That username is taken.")

    st.stop()


require_login()

def modes():
    mode = st.selectbox("Mode", ["Select a mode","Summary", "Flashcard", "Quiz", "Explain", "Trick Question", "chat", "doc stats", "Focus timer"])
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
            if st.download_button("Download Summary", summary, file_name="summary.txt"):
                st.success("Summary downloaded successfully!")
            
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
        # add a button to download the flashcards as a text file
        if st.button("Download Flashcards"):
            flashcard_text = "\n".join([f"Q: {q}\nA: {a}\n" for q, a in cards])
            if st.download_button("Download Flashcards", flashcard_text, file_name="flashcards.txt"):
                st.success("Flashcards downloaded successfully!")
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

        # add a button to download the quiz questions and answers as a text file
        if st.button("Download Quiz"):
            quiz_text = "\n".join([f"Q: {q}\nA: {a}\n" for q, a in cards])
            if st.download_button("Download Quiz", quiz_text, file_name="quiz.txt"):
                st.success("Quiz downloaded successfully!")
    if mode == "Explain":
        st.write("Explain mode selected.")
        # now using explain_text function to explain the text.
        with st.spinner("Generating explanation..."):
            explanation = explain_text(text)
            st.subheader("Explanation:")
            st.write(explanation)
            # add a button to download the explanation as a text file
            if st.download_button("Download Explanation", explanation, file_name="explanation.txt"):
                st.success("Explanation downloaded successfully!")
    if mode == "Trick Question":
        st.write("Trick Question mode selected.")
        if st.button("Generate trick questions"):
        # now using trick_questions function to generate trick questions from the text.
            with st.spinner("Generating trick questions..."):
                trick_qs = trick_questions(text)
                st.subheader("Trick Questions:")
                st.write(trick_qs)
                    # add a button to download the trick questions as a text file
                if st.download_button("Download Trick Questions", trick_qs, file_name="trick_questions.txt"):
                    st.success("Trick questions downloaded successfully!")
    ## chat operation mode!
    if mode == "chat":
        st.write("Chat mode selected.")
        # create a chat like interface where user can ask questions about the text and get answers based on the text using the chat_with_assistant function.
        question = st.text_input("Ask a question about the text:")
        if st.button("Ask"):
            with st.spinner("Getting answer..."):
                a = chat_with_assistant(text, question)
                st.subheader("Answer:")
                st.write(a)

    if mode == "Focus timer":
        st.write("Focus Timer mode selected.")
        st.write("Set a timer to focus on your study material without distractions.")
        minutes = st.slider("Enter focus time in minutes:", min_value=1, max_value=120, value=25)
        if st.button("Start Focus Timer"):
            st.success(f"Focus timer started for {minutes} minutes. Stay focused!")
# idk this just does some super basic text stats… like counting words,
# sentences, avg sentence length, nothing fancy at all. no api stuff,
# literally just splitting strings and doing a couple sums. could prob
# clean this up later but it works for now.
    if mode == "doc stats":
        st.write("Document Statistics mode selected.")
        word_count = len(text.split())
        sentence_count = len(text.split('.'))
        avg_sentence_length = word_count / sentence_count if sentence_count else 0
        read_time = word_count / 200  # assuming average reading speed of 200 wpm
        st.subheader("Document Statistics:")
        st.write(f"Word Count: {word_count}")
        st.write(f"Sentence Count: {sentence_count}")
        st.write(f"Average Sentence Length: {avg_sentence_length:.2f} words")
        st.write(f"Estimated Reading Time: {read_time:.2f} minutes")

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

