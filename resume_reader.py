import fitz

def read_resume():

    doc = fitz.open("data/resume.pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    return text