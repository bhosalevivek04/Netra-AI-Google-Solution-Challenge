# buttons/button_c.py

from utils.tts import speak_google
import subprocess
import time
from config import DEBOUNCE_TIME

def gemini_describe_image():
    speak_google("Capturing image for analysis")
    subprocess.run(["python", "gemini/gemini_image_describer.py"])
    speak_google("Image analysis complete")
    time.sleep(DEBOUNCE_TIME)