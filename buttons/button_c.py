# buttons/button_c.py

from utils.tts import speak_google
import subprocess
import time
import os
from config import DEBOUNCE_TIME, GEMINI_IMAGE_SCRIPT

def gemini_describe_image():
    try:
        if not os.path.exists(GEMINI_IMAGE_SCRIPT):
            speak_google("Error: Image analysis script not found")
            return

        speak_google("Capturing image for analysis")
        result = subprocess.run(
            ["python", GEMINI_IMAGE_SCRIPT],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            speak_google(f"Image analysis failed: {result.stderr}")
            return

        speak_google("Image analysis complete")
    except Exception as e:
        speak_google(f"System error: {str(e)}")
    finally:
        time.sleep(DEBOUNCE_TIME)
