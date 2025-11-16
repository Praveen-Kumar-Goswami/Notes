from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from firebase_admin import credentials, firestore, auth, initialize_app
import pyrebase

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

config = {
    "apiKey": "AIzaSyBhevkc0Foxzxxhd9RyUM5B254F9-b0rec",
    "authDomain": "my-med-app-c7880.firebaseapp.com",
    "projectId": "my-med-app-c7880",
    "storageBucket": "my-med-app-c7880.firebasestorage.app",
    "messagingSenderId": "1074750455581",
    "appId": "1:1074750455581:web:c22edd4d0454cd4c32abf4",
    "databaseURL": "https://my-med-app-c7880-default-rtdb.asia-southeast1.firebasedatabase.app"
}


firebase = pyrebase.initialize_app(config)
fb_auth = firebase.auth()

cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
firebase_admin = initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = fb_auth.sign_in_with_email_and_password(email, password)
        session['user'] = user['idToken']
        session['user_id'] = user['localId']
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    try:
        user = fb_auth.create_user_with_email_and_password(email, password)
        session['user'] = user['idToken']
        session['user_id'] = user['localId']
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    
    if request.method == 'GET':
        notes_ref = db.collection('users').document(user_id).collection('notes')
        docs = notes_ref.stream()
        notes_list = []
        for doc in docs:
            note_data = doc.to_dict()
            note_data['id'] = doc.id
            notes_list.append(note_data)
        return jsonify(notes_list)
    
    elif request.method == 'POST':
        data = request.json
        title = data.get('title', '')
        content = data.get('content', '')
        
        note_data = {
            'title': title,
            'content': content,
            'created': firestore.SERVER_TIMESTAMP,
            'updated': firestore.SERVER_TIMESTAMP
        }
        
        doc_ref = db.collection('users').document(user_id).collection('notes').document()
        doc_ref.set(note_data)
        
        return jsonify({"success": True, "id": doc_ref.id})

@app.route('/notes/<note_id>', methods=['PUT', 'DELETE'])
def note(note_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    user_id = session['user_id']
    note_ref = db.collection('users').document(user_id).collection('notes').document(note_id)
    
    if request.method == 'PUT':
        data = request.json
        updates = {
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'updated': firestore.SERVER_TIMESTAMP
        }
        note_ref.update(updates)
        return jsonify({"success": True})
    
    elif request.method == 'DELETE':
        note_ref.delete()
        return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)