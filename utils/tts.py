# utils/tts.py

from gtts import gTTS
import os

def speak_google(text):
    if not text:
        return
    tts = gTTS(text, lang='en')
    filename = "temp_tts.mp3"
    tts.save(filename)
    os.system(f"mpg123 -q {filename}")
    os.remove(filename)