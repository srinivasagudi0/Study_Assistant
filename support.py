# all important functions and intel stays here

# first task convert pdf to text
import PyPDF2

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
