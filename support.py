# all important functions and intel stays here

# first task convert pdf to text
import PyPDF2
import ast

def pdf_to_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# now be able to summarize the text using openai api (use a small llm model for now)
from openai import OpenAI
# i will call it yk.
def summarize_text(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # chnage this if you want to use a different model, but for now this is good for testing. I mean for summary it is fine.
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text for students. Be concise and clear."},
            {"role": "user", "content": f"Please summarize the following text: {text}"}
        ]
    )
    summary = response.choices[0].message.content
    return summary

# now be able to generate flashcards from the text using openai api (use a small llm model for now)
def generate_flashcards(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # chnage this if you want to use a different model, but for now this is good for testing. I mean for summary it is fine.
        messages=[
            {"role": "system", "content": """You are a helpful assistant that generates flashcards for students. Create flashcards in this format [
    ("What is 2+2?", "4"),
    ("What is the capital of France?", "Paris")
]"""},
            {"role": "user", "content": f"Generate flashcards from this text:\n\n{text}\n\n. Give atleast 5 flashcards. Or evem more but max is 15."}
        ]
    )
    content = (response.choices[0].message.content or "").strip()
    try:
        parsed = ast.literal_eval(content)
        if isinstance(parsed, list):
            cards = [(str(i[0]), str(i[1])) for i in parsed if isinstance(i, (list, tuple)) and len(i) == 2]
            if cards:
                return cards
    except Exception:
        pass
    return [("Flashcards", content)]
