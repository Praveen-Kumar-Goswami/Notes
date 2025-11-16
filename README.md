# Make A Note

A responsive web application for creating and managing notes using Flask, HTML, CSS, and Firebase.

## Features

- User authentication (Sign up/Login) using Firebase Authentication
- Create, read, update, and delete notes
- Responsive design that works on all devices
- Secure note storage in Firebase Firestore

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Firebase:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project
   - Enable Authentication (Email/Password)
   - Enable Firestore Database
   - Download your service account key as `firebase-config.json` and place it in the project root
   - Copy your Firebase web config and update `static/js/firebase-config.js` with your credentials

3. Set environment variables (optional):
   - Create a `.env` file with `SECRET_KEY=your-secret-key-here`

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
.
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── firebase-config.json   # Firebase service account key (not in repo)
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── notes.html
├── static/
│   ├── css/
│   │   └── style.css     # Responsive styles
│   └── js/
│       ├── firebase-config.js
│       ├── auth.js       # Authentication logic
│       └── notes.js      # Notes management
└── README.md
```

## Firebase Configuration

Update `static/js/firebase-config.js` with your Firebase web app configuration:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

## Notes

- Make sure to enable Email/Password authentication in Firebase Console
- Firestore security rules should allow authenticated users to read/write their own notes
- The app uses server-side session management for additional security


