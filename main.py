# main.py

import RPi.GPIO as GPIO
import time
from buttons import button_a, button_b, button_c, button_d
from utils.tts import speak_google

from config import (
    CAPTURE_BUTTON_PIN,
    RECOGNIZE_BUTTON_PIN,
    GEMINI_IMAGE_PIN,
    GEMINI_VIDEO_PIN
)

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CAPTURE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(RECOGNIZE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GEMINI_IMAGE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GEMINI_VIDEO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
    setup_gpio()
    speak_google("Netra AI system initialized")

    try:
        while True:
            if GPIO.input(CAPTURE_BUTTON_PIN) == GPIO.LOW:
                button_a.capture_and_train()
            if GPIO.input(RECOGNIZE_BUTTON_PIN) == GPIO.LOW:
                button_b.toggle_recognize()
            if GPIO.input(GEMINI_IMAGE_PIN) == GPIO.LOW:
                button_c.gemini_describe_image()

            button_d.handle_button_d()
            time.sleep(0.1)

    except KeyboardInterrupt:
        speak_google("System shutting down")
    finally:
        button_b.cleanup()
        GPIO.cleanup()

if __name__ == "__main__":
    main()