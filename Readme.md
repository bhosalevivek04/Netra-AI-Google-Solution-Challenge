# 🚨 Netra AI – Smart Face Recognition & Emergency Assistant

**Netra AI** is a Raspberry Pi-based intelligent assistant designed for real-time **face recognition**, **Gemini AI-based scene analysis**, and **emergency alert handling** via physical buttons. It’s a modular and scalable project designed to help users in critical situations with voice feedback.

---

## 💡 Features

- **Button A (GPIO 17)** – Capture face and train model.
- **Button B (GPIO 18)** – Toggle real-time face recognition.
- **Button C (GPIO 22)** – Capture image and describe it using Gemini AI.
- **Button D (GPIO 23)**  
  - **Short press** – Record a video and describe the scene via Gemini AI.  
  - **Long press (≥ 3 sec)** – Send emergency alert to backend (Node.js + Twilio) via HTTP.

All responses are given through **Bluetooth-connected speaker** using **gTTS text-to-speech**.

---

## 🧠 Technologies Used

- Raspberry Pi GPIO (Button interfacing)
- Python
- Node.js (Twilio SMS backend)
- gTTS + mpg123 (for speech output)
- Gemini 1.5 Pro (Image/Video analysis)
- OpenCV (Face recognition pipeline)
- Twilio (SMS Alerts)

---

## 📁 Folder Structure

```
netra_ai/
├── main.py
├── config.py
├── buttons/
│   ├── button_a.py               # Face capture + training
│   ├── button_b.py               # Toggle recognition
│   ├── button_c.py               # Gemini image describer
│   ├── button_d.py               # Gemini video + Emergency trigger
├── utils/
│   ├── tts.py                    # gTTS-based voice module
│   ├── emergency.py             # HTTP trigger for SMS backend
├── gemini/
│   ├── gemini_image_describer.py  # Describe image using Gemini
│   ├── gemini_video_describer.py  # Describe video using Gemini
├── sms-backend/                 # Node.js Twilio SMS backend
│   ├── index.js
│   ├── .env
│   ├── package.json
│   └── README.md
├── README.md                    # Project Documentation
```

---

## ⚙️ Setup Instructions (Raspberry Pi)

### 1. Install Python dependencies:
```bash
sudo apt update
sudo apt install mpg123
pip install gTTS RPi.GPIO requests
```

### 2. Prepare face recognition module:
Place your script `face_rec.py` that supports:
- `python3 face_rec.py capture`
- `python3 face_rec.py train`
- `python3 face_rec.py recognize`

### 3. Add Gemini AI scripts:
Place these inside `gemini/` directory:
- `gemini_image_describer.py`
- `gemini_video_describer.py`

### 4. Run the main controller:
```bash
python3 main.py
```

---

## 📡 Setup for Emergency SMS Backend

### 1. Go to `sms-backend/` folder:
```bash
cd sms-backend/
```

### 2. Install dependencies:
```bash
npm install
```

### 3. Create `.env` file with Twilio keys:
```
ACCOUNT_SID=your_twilio_account_sid
AUTH_TOKEN=your_twilio_auth_token
FROM_NUMBER=+1234567890        # Twilio verified number
TO_NUMBER=+9198XXXXXXXX        # Emergency receiver number
DEFAULT_MESSAGE=URGENT: I need help immediately...
```

### 4. Start backend server:
```bash
node index.js
```

### 5. Update the Raspberry Pi config:
In `config.py`, set:
```python
EMERGENCY_ENDPOINT = "http://<your_pi_ip>:3000/data"
```

---

## 🧪 Test Your Setup

- ✅ Press **Button A** → Face capture & training  
- ✅ Press **Button B** → Toggle face recognition (gives voice feedback)  
- ✅ Press **Button C** → Captures image, describes with Gemini  
- ✅ Press **Button D (short)** → Records short video, analyzes with Gemini  
- ✅ Press **Button D (long)** → Sends emergency alert via Twilio  

---

## 📌 Notes

- Ensure your buttons are connected properly on the GPIO pins.
- Bluetooth speaker must be paired before running `main.py`.
- Twilio trial accounts require verified phone numbers.
- Gemini API usage is simulated unless fully implemented with API credentials.

---