# utils/tts.py

from gtts import gTTS
import os
import tempfile
import subprocess
import time

def speak_google(text):
    if not text:
        return
        
    try:
        # Check if mpg123 is installed
        try:
            subprocess.run(["which", "mpg123"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            print("Error: mpg123 not found. Please install with: sudo apt install mpg123")
            return

        # Create unique temp file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name
            
        # Generate speech
        tts = gTTS(text=text, lang='en')
        tts.save(temp_path)
        
        # Play audio
        subprocess.run(["mpg123", "-q", temp_path], check=True)
        
    except Exception as e:
        print(f"TTS Error: {str(e)}")
    finally:
        # Clean up temp file
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
