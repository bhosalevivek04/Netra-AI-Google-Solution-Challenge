#!/usr/bin/env python3

import cv2
import base64
import requests
import pygame
import os
import time
import tempfile
from io import BytesIO
from gtts import gTTS

##########################
# 1) Gemini & TTS Config
##########################
GEMINI_API_KEY = ""  # Replace with your real key
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key="
    + GEMINI_API_KEY
)

def capture_image():
    """
    Capture an image from a USB camera using OpenCV and return base64-encoded data.
    """
    # Attempt to open the USB camera (device index 0)
    # If it's not recognized at 0, try 1 or 2
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # V4L2 backend often works well on Pi
    if not cap.isOpened():
        print("Error: Could not open USB camera.")
        return None
    
    # Set a reasonable resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("Error: Failed to capture image from USB camera.")
        return None
    
    # Save the image to a temporary file
    temp_path = "/tmp/webcam_capture.jpg"
    cv2.imwrite(temp_path, frame)
    
    # Convert the image to base64
    with open(temp_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")
    
    # (Optionally remove local file)
    # os.remove(temp_path)
    
    return base64_image

def send_to_gemini_api(base64_image):
    """
    Send the base64-encoded image to the Gemini endpoint and return the text description.
    """
    # Build the JSON payload
    payload = {
        "contents": [{
            "parts": [
                {"text": "Describe this image in short"},  # Prompt
                {
                    "inlineData": {
                        "mimeType": "image/jpeg",
                        "data": base64_image
                    }
                }
            ]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        response_json = response.json()
        # Parse the nested structure
        candidates = response_json.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if parts:
                return parts[0].get("text", "No description available.")
        return "No candidates found."
    else:
        print("Error from Gemini API:", response.text)
        return "Failed to get response from Gemini."

def play_tts(text):
    """
    Convert text to speech using gTTS and play via pygame.
    This avoids the unofficial Google Translate TTS endpoint,
    preventing 400 errors for longer or special text.
    """
    if not text:
        return
    
    try:
        # Create a temporary MP3 file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
            tts = gTTS(text=text, lang='en')
            tts.save(temp_audio.name)
            
            # Initialize pygame mixer
            pygame.mixer.init()
            pygame.mixer.music.load(temp_audio.name)
            pygame.mixer.music.play()
            
            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        # Quit the mixer
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error in TTS playback: {str(e)}")

def main():
    print("USB Camera Image Describer for Raspberry Pi")

    # 1) Capture the image from USB camera
    base64_image = capture_image()
    if not base64_image:
        return
    
    # 2) Send to Gemini
    description = send_to_gemini_api(base64_image)
    print("Gemini says:", description)
    
    # 3) Speak the description (via local gTTS approach)
    play_tts(description)

if __name__ == "__main__":
    main()
