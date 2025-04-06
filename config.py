# System Configuration
# config.py

# GPIO Pin Configuration
CAPTURE_BUTTON_PIN = 17
RECOGNIZE_BUTTON_PIN = 18
GEMINI_IMAGE_PIN = 22
GEMINI_VIDEO_PIN = 23
DEBOUNCE_TIME = 1

# Script Paths
FACE_REC_SCRIPT = "face_rec.py"
GEMINI_IMAGE_SCRIPT = "gemini/gemini_image_describer.py"
GEMINI_VIDEO_SCRIPT = "gemini/gemini_video_describer.py"

# API Endpoints
EMERGENCY_ENDPOINT = "http://localhost:3000/data"
