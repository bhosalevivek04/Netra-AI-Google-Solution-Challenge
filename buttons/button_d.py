# buttons/button_d.py

from utils.tts import speak_google
from utils.emergency import send_emergency_sms
import time
import RPi.GPIO as GPIO
import subprocess
import os
from config import GEMINI_VIDEO_PIN, DEBOUNCE_TIME, GEMINI_VIDEO_SCRIPT

button_d_pressed = False
button_d_start_time = 0
last_trigger_time = 0
MIN_EMERGENCY_INTERVAL = 30  # Minimum 30 seconds between emergency triggers

def gemini_describe_video():
    try:
        if not os.path.exists(GEMINI_VIDEO_SCRIPT):
            speak_google("Error: Video analysis script not found")
            return

        speak_google("Recording video for analysis")
        result = subprocess.run(
            ["python", GEMINI_VIDEO_SCRIPT],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            speak_google(f"Video analysis failed: {result.stderr}")
            return

        speak_google("Video analysis finished")
    except Exception as e:
        speak_google(f"System error: {str(e)}")

def handle_button_d():
    global button_d_pressed, button_d_start_time, last_trigger_time
    current_state = GPIO.input(GEMINI_VIDEO_PIN)
    current_time = time.time()

    if current_state == GPIO.LOW:
        if not button_d_pressed:
            button_d_pressed = True
            button_d_start_time = current_time
    else:
        if button_d_pressed:
            duration = current_time - button_d_start_time
            button_d_pressed = False
            
            if duration >= 3:
                # Emergency trigger
                if current_time - last_trigger_time < MIN_EMERGENCY_INTERVAL:
                    speak_google("Emergency alert already sent recently")
                    return
                last_trigger_time = current_time
                send_emergency_sms()
            else:
                # Video analysis
                gemini_describe_video()
            
            time.sleep(DEBOUNCE_TIME)
