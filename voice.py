# voice.py
import speech_recognition as sr

def speech_to_text():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        return r.recognize_google(audio)
    except (OSError, AttributeError) as e:
        # No mic hardware available (e.g. cloud deployment)
        return None