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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Get from environment variable
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    exit(1)
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key="
    + GEMINI_API_KEY
)

def capture_video(duration=5):
    """
    Capture a short video (e.g., 5 seconds) from the USB camera using OpenCV.
    Save it as an MP4 (H264 or MJPEG) in /tmp, then return the base64-encoded file data.
    """
    # Attempt to open the USB camera (device index 0)
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    if not cap.isOpened():
        print("Error: Could not open USB camera.")
        return None
    
    # Set a reasonable resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Define the codec and create VideoWriter
    # On Raspberry Pi, use 'XVID' or 'MJPG' if 'mp4v' doesn't work
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    temp_path = "/tmp/webcam_capture.mp4"
    out = cv2.VideoWriter(temp_path, fourcc, 20.0, (640, 480))
    
    start_time = time.time()
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture video frame.")
            break
        out.write(frame)
    
    cap.release()
    out.release()
    
    # Read the MP4 file, convert to base64
    if not os.path.exists(temp_path):
        print("Video file not created.")
        return None
    
    with open(temp_path, "rb") as vid_file:
        base64_video = base64.b64encode(vid_file.read()).decode("utf-8")
    
    # (Optionally remove local file)
    # os.remove(temp_path)
    
    return base64_video

def send_to_gemini_api_video(base64_video, max_retries=3):
    """
    Send the base64-encoded video to the Gemini endpoint with retry logic.
    Returns the text description or error message.
    """
    for attempt in range(max_retries):
        try:
            # Build the JSON payload for video
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "Describe this video in short"},
                        {
                            "inlineData": {
                                "mimeType": "video/mp4",
                                "data": base64_video
                            }
                        }
                    ]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            response = requests.post(GEMINI_API_URL, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                response_json = response.json()
                candidates = response_json.get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        return parts[0].get("text", "No description available.")
                return "No candidates found."
            
            elif response.status_code >= 500:
                print(f"Server error (attempt {attempt + 1}/{max_retries}): {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue
                
            else:
                print(f"API error: {response.text}")
                return "Failed to get response from Gemini."

        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            continue

    return "Failed to get response after multiple attempts."

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
    print("USB Camera Video Describer for Raspberry Pi")

    # 1) Capture a short video (5 seconds by default)
    base64_video = capture_video(duration=5)
    if not base64_video:
        return
    
    # 2) Send to Gemini
    description = send_to_gemini_api_video(base64_video)
    print("Gemini says:", description)
    
    # 3) Speak the description (via local gTTS approach)
    play_tts(description)

if __name__ == "__main__":
    main()
