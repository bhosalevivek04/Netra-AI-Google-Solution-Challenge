# utils/emergency.py

from config import EMERGENCY_ENDPOINT
from utils.tts import speak_google
import requests
import time

last_sms_time = 0
MIN_SMS_INTERVAL = 30  # Minimum 30 seconds between emergency SMS

def send_emergency_sms():
    global last_sms_time
    current_time = time.time()
    
    if current_time - last_sms_time < MIN_SMS_INTERVAL:
        speak_google("Emergency alert already sent recently")
        return
        
    speak_google("Emergency alert triggered")
    try:
        response = requests.post(EMERGENCY_ENDPOINT, timeout=5)
        if response.status_code == 200:
            speak_google("Emergency message sent successfully")
            last_sms_time = current_time
        else:
            speak_google(f"Failed to send emergency message: Status {response.status_code}")
    except requests.exceptions.Timeout:
        speak_google("Emergency service timeout")
    except requests.exceptions.RequestException as e:
        speak_google(f"Emergency service error: {str(e)}")
