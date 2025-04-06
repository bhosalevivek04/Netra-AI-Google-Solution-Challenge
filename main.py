# main.py

import RPi.GPIO as GPIO
import time
import logging
from buttons import button_a, button_b, button_c, button_d
from utils.tts import speak_google
from config import (
    CAPTURE_BUTTON_PIN,
    RECOGNIZE_BUTTON_PIN,
    GEMINI_IMAGE_PIN,
    GEMINI_VIDEO_PIN
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('netra_ai.log'),
        logging.StreamHandler()
    ]
)

def setup_gpio():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CAPTURE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RECOGNIZE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GEMINI_IMAGE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(GEMINI_VIDEO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        logging.info("GPIO setup completed successfully")
    except Exception as e:
        logging.error(f"GPIO setup failed: {str(e)}")
        raise

def main():
    try:
        setup_gpio()
        speak_google("Netra AI system initialized")
        logging.info("System initialized")

        while True:
            try:
                if GPIO.input(CAPTURE_BUTTON_PIN) == GPIO.LOW:
                    button_a.capture_and_train()
                if GPIO.input(RECOGNIZE_BUTTON_PIN) == GPIO.LOW:
                    button_b.toggle_recognize()
                if GPIO.input(GEMINI_IMAGE_PIN) == GPIO.LOW:
                    button_c.gemini_describe_image()

                button_d.handle_button_d()
                time.sleep(0.1)

            except Exception as e:
                logging.error(f"Error in main loop: {str(e)}")
                speak_google("System error occurred")
                time.sleep(1)  # Prevent rapid error loops

    except KeyboardInterrupt:
        logging.info("Shutdown initiated by user")
        speak_google("System shutting down")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        speak_google("Critical system failure")
    finally:
        try:
            button_b.cleanup()
            GPIO.cleanup()
            logging.info("System shutdown complete")
        except Exception as e:
            logging.error(f"Cleanup error: {str(e)}")

if __name__ == "__main__":
    main()
