# buttons/button_b.py

from utils.tts import speak_google
import subprocess
import time
from config import DEBOUNCE_TIME

recognize_process = None

def toggle_recognize():
    global recognize_process
    if recognize_process is None:
        speak_google("Starting real time recognition")
        recognize_process = subprocess.Popen(["python", "face_rec.py", "recognize"])
    else:
        speak_google("Recognition ended")
        recognize_process.terminate()
        recognize_process = None
    time.sleep(DEBOUNCE_TIME)

def cleanup():
    global recognize_process
    if recognize_process:
        recognize_process.terminate()