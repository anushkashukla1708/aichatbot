from gtts import gTTS
import streamlit as st
import tempfile


def speak(text):

    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as file:
        audio_path = file.name
        tts.save(audio_path)

    with open(audio_path, "rb") as audio:
        st.audio(audio.read(), format="audio/mp3")