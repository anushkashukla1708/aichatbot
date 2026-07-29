from gtts import gTTS
import streamlit as st
import tempfile


def speak(text):

    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)

        audio_file = open(fp.name, "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")