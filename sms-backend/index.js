require('dotenv').config();
const express = require('express');
const twilio = require('twilio');

const accountSid = process.env.ACCOUNT_SID;
const authToken = process.env.AUTH_TOKEN;
const fromNumber = process.env.FROM_NUMBER;
const toNumber = process.env.TO_NUMBER;
const defaultMessage = process.env.DEFAULT_MESSAGE || 
  "URGENT: I need help immediately. I am in a dangerous situation and unable to secure my own safety. Please send emergency assistance to my location as soon as possible.";

const client = new twilio(accountSid, authToken);
const app = express();

app.post('/data', (req, res) => {
    client.messages.create({
        body: defaultMessage,
        to: toNumber,       
        from: fromNumber    
    })
    .then((smsResponse) => {
        console.log(`Message sent with SID: ${smsResponse.sid}`);
        res.status(200).json({ message: 'Emergency SMS sent successfully.', sid: smsResponse.sid });
    })
    .catch((error) => {
        console.error('Error sending SMS:', error);
        res.status(500).json({ error: 'Failed to send emergency SMS.', details: error.message });
    });
});


const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Emergency SMS server running on port ${PORT}`);
});