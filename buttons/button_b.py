# buttons/button_b.py

from utils.tts import speak_google
import subprocess
import time
import os
from config import DEBOUNCE_TIME, FACE_REC_SCRIPT

recognize_process = None

def toggle_recognize():
    global recognize_process
    try:
        if not os.path.exists(FACE_REC_SCRIPT):
            speak_google("Error: Face recognition script not found")
            return

        if recognize_process is None:
            speak_google("Starting real time recognition")
            recognize_process = subprocess.Popen(
                ["python", FACE_REC_SCRIPT, "recognize"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            speak_google("Recognition ended")
            cleanup()
    except Exception as e:
        speak_google(f"System error: {str(e)}")
    finally:
        time.sleep(DEBOUNCE_TIME)

def cleanup():
    global recognize_process
    if recognize_process:
        recognize_process.terminate()
        recognize_process = None
