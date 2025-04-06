# buttons/button_a.py

from utils.tts import speak_google
import subprocess
import time
from config import DEBOUNCE_TIME

def capture_and_train():
    speak_google("Starting face capture and training")
    subprocess.run(["python", "face_rec.py", "capture"])
    speak_google("Capture complete. Starting training.")
    subprocess.run(["python", "face_rec.py", "train"])
    speak_google("Training completed successfully")
    time.sleep(DEBOUNCE_TIME)