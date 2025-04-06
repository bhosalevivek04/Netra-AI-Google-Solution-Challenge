# utils/emergency.py

from config import EMERGENCY_ENDPOINT
from utils.tts import speak_google
import requests

def send_emergency_sms():
    speak_google("Emergency alert triggered")
    try:
        response = requests.post(EMERGENCY_ENDPOINT, timeout=5)
        if response.status_code == 200:
            speak_google("Emergency message sent successfully")
        else:
            speak_google("Failed to send emergency message")
    except Exception:
        speak_google("Emergency service unavailable")