import os

from dotenv import load_dotenv
from google import genai

from prompts import SYSTEM_PROMPT
from rag.search import retrieve
from rag.resume_search import retrieve_resume
from resume_reader import read_resume


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

if not question or not question.strip():
    return "Please ask a question."
def ask_anushka_gpt(question, history):

    if not question or not question.strip():
        return "Please ask a question."

    # Retrieve relevant documents
    portfolio_docs = retrieve(question)
    resume_docs = retrieve_resume(question)

    print("\n========== Retrieved Documents ==========")
    for doc in portfolio_docs:
        print(doc["title"])

    portfolio = "\n\n".join(
        f"{doc['title']}\n{doc['text']}"
        for doc in portfolio_docs
    )

    resume_docs_text = "\n\n".join(
        f"{doc['title']}\n{doc['text']}"
        for doc in resume_docs
    )

    # Read Resume
    resume = read_resume()
    




    # Prompt
    prompt = f"""
{SYSTEM_PROMPT}

Portfolio Information

{portfolio}

Resume Information

{resume}

Answer naturally.

Do not output JSON.

If the answer isn't available,
say you don't know.
"""

    contents = [
        {
            "role": "user",
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]

    # Previous Conversation
    for msg in history:

        role = "model" if msg["role"] == "assistant" else "user"

        contents.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": msg["content"]
                    }
                ]
            }
        )

    # Current Question
    contents.append(
        {
            "role": "user",
            "parts": [
                {
                    "text": question
                }
            ]
        }
    )

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=contents
        )

        sources = ", ".join(
            doc["title"] for doc in portfolio_docs
        )

        final_answer = f"""{response.text}

---
📚 **Sources Used:** {sources}
"""

        # Speak the answer
        

        return final_answer

    except Exception as e:

        print("\n========== Gemini Error ==========")
        print(e)

        return f"Error: {e}"


if __name__ == "__main__":

    history = []

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        answer = ask_anushka_gpt(
            question,
            history
        )

        print("\nAnushkaGPT:\n")
        print(answer)

        history.append(
            {
                "role": "user",
                "content": question
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )