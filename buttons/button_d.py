# buttons/button_d.py

from utils.tts import speak_google
from utils.emergency import send_emergency_sms
import time
import RPi.GPIO as GPIO
import subprocess
from config import GEMINI_VIDEO_PIN, DEBOUNCE_TIME

button_d_pressed = False
button_d_start_time = 0

def gemini_describe_video():
    speak_google("Recording video for analysis")
    subprocess.run(["python", "gemini/gemini_video_describer.py"])
    speak_google("Video analysis finished")
    time.sleep(DEBOUNCE_TIME)

def handle_button_d():
    global button_d_pressed, button_d_start_time
    current_state = GPIO.input(GEMINI_VIDEO_PIN)

    if current_state == GPIO.LOW:
        if not button_d_pressed:
            button_d_pressed = True
            button_d_start_time = time.time()
    else:
        if button_d_pressed:
            duration = time.time() - button_d_start_time
            button_d_pressed = False
            if duration >= 3:
                send_emergency_sms()
            else:
                gemini_describe_video()
            time.sleep(DEBOUNCE_TIME)