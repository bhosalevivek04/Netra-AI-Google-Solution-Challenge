# Netra AI Vision Assistance System

## Complete Project Structure
```
netra-ai/
├── buttons/               # Button handler modules
│   ├── button_a.py        # Face capture & training
│   ├── button_b.py        # Recognition toggle
│   ├── button_c.py        # Image description
│   └── button_d.py        # Emergency/Videodescription
├── gemini/                # AI integration
│   ├── gemini_image_describer.py
│   └── gemini_video_describer.py
├── utils/                 # Utility modules
│   ├── tts.py             # Text-to-speech
│   └── emergency.py       # SMS alert handling
├── sms-backend/           # Node.js SMS service
│   ├── index.js           # SMS server
│   ├── package.json       # Dependencies
│   ├── package-lock.json
│   └── README.md          # SMS specific docs
├── main.py                # Main application
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
└── README.md              # This document
```

## SMS Backend Service

### Key Features
- Twilio integration for emergency SMS
- Rate limiting (max 1 alert every 30 minutes)
- Location data support
- Multiple emergency contacts

### Setup Instructions
1. Install Node.js v16+:
```bash
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs
```

2. Configure SMS service:
```bash
cd sms-backend
npm install
cp .env.example .env
```

3. Edit `.env` with your:
```env
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+123456789
EMERGENCY_CONTACTS=+15555555555,+16666666666
```

4. Start the service:
```bash
node index.js
```

## Main System Installation

### Hardware Requirements
- Raspberry Pi 4 (recommended)
- USB Webcam
- 4x Tactile buttons
- Audio output device
- SIM card module (for SMS)

### Software Setup
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip mpg123 python3-opencv

# Python packages
pip install -r requirements.txt

# Set environment variables
echo "export GEMINI_API_KEY='your_api_key'" >> ~/.bashrc
echo "export EMERGENCY_SMS_ENDPOINT='http://your-server:3000/alert'" >> ~/.bashrc
source ~/.bashrc
```

## Running the System
1. Start SMS backend (separate terminal):
```bash
cd sms-backend && node index.js
```

2. Start main application:
```bash
python main.py
```

## Troubleshooting Guide


### Camera Problems
```bash
# Verify camera detection
ls /dev/video*
# Test camera capture
raspistill -v -o test.jpg
```

### Audio Issues
```bash
# Test audio playback
speaker-test -t wav -c 2
# Check mpg123 installation
which mpg123
```
