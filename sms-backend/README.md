# 🚨 Emergency SMS Backend (Twilio)

This Node.js server handles emergency alert requests by sending SMS messages using the Twilio API. It is used in the **Netra AI** project to send alerts when a long-press is detected.

---

## 📦 Tech Stack

- Node.js
- Express.js
- Twilio API

---

## ⚙️ Setup Instructions

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create `.env` file** in the same directory:
   ```env
   ACCOUNT_SID=your_twilio_sid
   AUTH_TOKEN=your_twilio_token
   FROM_NUMBER=+1XXXXXXXXXX
   TO_NUMBER=+91XXXXXXXXXX
   DEFAULT_MESSAGE=This is an emergency message
   PORT=3000
   ```

3. **Run the server:**
   ```bash
   node index.js
   ```

---

## 🔌 API Endpoint

### `POST /data`

Sends an SMS to the configured number.

**Response:**
- `200 OK` – Message sent successfully
- `500 Error` – Failed to send message

---

## 🔐 Security

- Don't expose `.env` file on public repositories.
- Use proper environment variable management for production.

---