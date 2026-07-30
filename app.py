# ---------------- SHOW OLD CHATS ---------------- #
# ---------------- SHOW OLD CHATS ---------------- #
import time

import streamlit as st

from chatbot import ask_anushka_gpt
from pdf import save_chat
from voice import speech_to_text
from memory import clear_history

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AnushkaGPT",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ---------------- #

with open("styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------- SESSION ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome Screen

if len(st.session_state.messages) == 0:

    st.info(
        """
# 👋 Welcome to AnushkaGPT

I can answer questions about:

- 👩 About Me
- 💼 Projects
- 🛠 Skills
- 🎓 Education
- 🏢 Experience
- 📄 Resume
- 📧 Contact Information

Ask me anything!
"""
    )

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.markdown("""
# 🤖 AnushkaGPT

### AI Portfolio Assistant

Powered by

✅ Gemini AI

✅ FAISS RAG

✅ Resume Parser

✅ Portfolio API
""")

    st.write(
        "Your Personal AI Portfolio Assistant"
    )

    st.divider()

    st.subheader("💡 Example Questions")

    st.write("• Tell me about yourself")
    st.write("• What projects have you built?")
    st.write("• What are your skills?")
    st.write("• Tell me about Verdict Lens")
    st.write("• Show your education")
    st.write("• Internship experience")

    st.success("🟢 AI Online")
    st.divider()

    if st.button("🗑 Clear Chat", key="clear_chat_btn"):

        st.session_state.messages = []

        clear_history()

        st.rerun()

    if st.button("📄 Download Chat", key="download_chat_btn"):

        save_chat(
            st.session_state.messages
        )

    st.divider()

    st.subheader("📊 Statistics")

    users = len(
        [
            x for x in st.session_state.messages
            if x["role"] == "user"
        ]
    )

    ai = len(
        [
            x for x in st.session_state.messages
            if x["role"] == "assistant"
        ]
    )

    st.metric("Questions", users)
    st.metric("Responses", ai)

    st.divider()

    st.success("🟢 AI Online")

    st.caption(
        "Powered by Gemini + FAISS"
    )

    st.divider()

    st.subheader("🛠 Tech Stack")

    st.markdown("""
- Gemini AI
- Streamlit
- Python
- FAISS
- Sentence Transformers
- Resume Parsing
- Portfolio API
""")

# ---------------- TITLE ---------------- #
st.markdown("""
### 👋 Welcome!

I'm **AnushkaGPT**, an AI assistant that can answer
questions about Anushka Shukla's:

- 🎓 Education
- 💼 Experience
- 🚀 Projects
- 🛠 Skills
- 📄 Resume
- 📧 Contact Information

Ask me anything below 👇
""")

st.caption(
    "Ask anything about Anushka Shukla"
)

# ---------------- QUICK QUESTIONS ---------------- #

st.write("### 💡 Quick Questions")

c1, c2 = st.columns(2)

with c1:

    if st.button("🙋 About Me", key="about_top"):
        st.session_state.question = "Tell me about yourself"
        st.rerun()
    if st.button("💼 Projects", key="projects_top"):
        st.session_state.question = "Tell me about your projects"
        st.rerun()
    if st.button("🛠 Skills", key="skills_top"):
        st.session_state.question = "What are your skills?"
        st.rerun()

with c2:

    if st.button("🎓 Education", key="education_top"):
        st.session_state.question = "Tell me about your education"
        st.rerun()
    if st.button("🏢 Experience", key="experience_top"):
        st.session_state.question = "Tell me about your internship"
        st.rerun()
    if st.button("📧 Contact", key="contact_top"):
        st.session_state.question = "How can I contact you?"
        st.rerun()

for message in st.session_state.messages:

    avatar = "👩" if message["role"] == "user" else "🤖"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# ---------------- VOICE INPUT ---------------- #

col1, col2 = st.columns([6, 1])

with col2:

    if st.button("🎤", key="voice_input_btn"):

        spoken = speech_to_text()

        if spoken:

            st.session_state.question = spoken

            st.rerun()


# ---------------- USER INPUT ---------------- #

typed_question = st.chat_input(
    "Ask anything about Anushka..."
)

question = None

if "question" in st.session_state:

    question = st.session_state.question

    del st.session_state.question

if typed_question:

    question = typed_question


# ---------------- CHATBOT ---------------- #

if question:

    # Save User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user",
        avatar="👩"
    ):
        st.markdown(question)

    # AI Reply

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        placeholder = st.empty()

        with st.status(
            "🤖 Processing...",
            expanded=True
        ) as status:

            st.write("🔍 Searching Portfolio...")
            time.sleep(0.3)

            st.write("📄 Reading Resume...")
            time.sleep(0.3)

            st.write("🧠 Searching FAISS Vector Database...")
            time.sleep(0.3)

            st.write("✨ Generating Response...")

            start = time.time()

            answer = ask_anushka_gpt(
                question,
                st.session_state.messages
            )

            elapsed = time.time() - start

            status.update(
                label=f"✅ Done ({elapsed:.2f}s)",
                state="complete"
            )

        streamed = ""

        for word in answer.split():

            streamed += word + " "

            placeholder.markdown(
                streamed + "▌"
            )

            if word.endswith("."):

                time.sleep(0.12)

            elif word.endswith(","):

                time.sleep(0.06)

            else:

                time.sleep(0.02)

        placeholder.markdown(streamed)

        st.caption(
            f"⚡ Response generated in {elapsed:.2f} sec"
        )

        st.code(
            answer,
            language="markdown"
        )

    # Save AI Response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ---------------- SUGGESTED QUESTIONS ---------------- #

st.divider()

st.write("### 💡 Suggested Questions")

c1, c2, c3 = st.columns(3)

with c1:

    if st.button(
        "📂 Projects",
        use_container_width=True,
        key="projects_suggested"
    ):

        st.session_state.question = (
            "Tell me about your projects"
        )

        st.rerun()

with c2:

    if st.button(
        "🛠 Skills",
        use_container_width=True,
        key="skills_suggested"
    ):

        st.session_state.question = (
            "What are your skills?"
        )

        st.rerun()

with c3:

    if st.button(
        "🎓 Education",
        use_container_width=True,
        key="education_suggested"
    ):

        st.session_state.question = (
            "Tell me about your education"
        )

        st.rerun()

st.write("")

c4, c5, c6 = st.columns(3)

with c4:

    if st.button(
        "🏢 Experience",
        use_container_width=True,
        key="experience_suggested"
    ):

        st.session_state.question = (
            "Tell me about your internship experience"
        )

        st.rerun()

with c5:

    if st.button(
        "🤖 Verdict Lens",
        use_container_width=True,
        key="verdict_lens_suggested"
    ):

        st.session_state.question = (
            "Explain your Verdict Lens project"
        )

        st.rerun()

with c6:

    if st.button(
        "📧 Contact",
        use_container_width=True,
        key="contact_suggested"
    ):

        st.session_state.question = (
            "How can I contact you?"
        )

        st.rerun()


# ---------------- FOOTER ---------------- #

st.divider()

st.markdown(
"""
<div style="text-align:center;padding:25px;">

<h4>🤖 AnushkaGPT</h4>

<p>
An AI-powered personal portfolio assistant built using
Gemini AI, Retrieval-Augmented Generation (RAG),
FAISS Vector Search, Resume Parsing, Streamlit,
and a Portfolio API.
</p>

<p>

🤖 Gemini AI &nbsp; | &nbsp;
🔍 FAISS RAG &nbsp; | &nbsp;
📄 Resume Parser &nbsp; | &nbsp;
🌐 Portfolio API &nbsp; | &nbsp;
⚡ Streamlit

</p>

<hr>

<p>

Made with ❤️ by <b>Anushka Shukla</b>

</p>

<p style="font-size:14px;color:gray;">

© 2026 All Rights Reserved

</p>

</div>
""",
unsafe_allow_html=True
)

st.write("### 🚀 Try asking")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("👩 About Me", use_container_width=True, key="about_bottom"):
        st.session_state.question = "Tell me about yourself"
        st.rerun()

with col2:

    if st.button("💼 Projects", use_container_width=True, key="projects_bottom"):
        st.session_state.question = "Tell me about your projects"
        st.rerun()

with col3:

    if st.button("🛠 Skills", use_container_width=True, key="skills_bottom"):
        st.session_state.question = "What are your skills?"
        st.rerun()