from flask import Flask, render_template, request, jsonify, session
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

if not firebase_admin._apps:
    fbCredJson = os.getenv('FIREBASE_CREDENTIALS')
    if fbCredJson:
        credDict = json.loads(fbCredJson)
        cred = credentials.Certificate(credDict)
    else:
        cred = credentials.Certificate('firebase-config.json')
    firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/api/verify-token', methods=['POST'])
def verify_token():
    try:
        data = request.json
        token = data.get('token')
        if not token:
            return jsonify({'error': 'No token provided'}), 400
        
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        session['uid'] = uid
        return jsonify({'uid': uid, 'email': decoded_token.get('email')}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True}), 200

@app.route('/api/notes', methods=['GET'])
def get_notes():
    try:
        uid = session.get('uid')
        if not uid:
            return jsonify({'error': 'Not authenticated'}), 401
        
        notes_ref = db.collection('notes').where('uid', '==', uid).order_by('created', direction=firestore.Query.DESCENDING)
        docs = notes_ref.stream()
        notes = []
        for doc in docs:
            note_data = doc.to_dict()
            note_data['id'] = doc.id
            notes.append(note_data)
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
def create_note():
    try:
        uid = session.get('uid')
        if not uid:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.json
        note_data = {
            'uid': uid,
            'title': data.get('title', ''),
            'content': data.get('content', ''),
            'created': firestore.SERVER_TIMESTAMP,
            'updated': firestore.SERVER_TIMESTAMP
        }
        doc_ref = db.collection('notes').add(note_data)
        note_data['id'] = doc_ref[1].id
        return jsonify(note_data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['PUT'])
def update_note(note_id):
    try:
        uid = session.get('uid')
        if not uid:
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.json
        note_ref = db.collection('notes').document(note_id)
        note_doc = note_ref.get()
        
        if not note_doc.exists:
            return jsonify({'error': 'Note not found'}), 404
        
        note_data = note_doc.to_dict()
        if note_data.get('uid') != uid:
            return jsonify({'error': 'Unauthorized'}), 403
        
        update_data = {
            'title': data.get('title', note_data.get('title', '')),
            'content': data.get('content', note_data.get('content', '')),
            'updated': firestore.SERVER_TIMESTAMP
        }
        note_ref.update(update_data)
        update_data['id'] = note_id
        return jsonify(update_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        uid = session.get('uid')
        if not uid:
            return jsonify({'error': 'Not authenticated'}), 401
        
        note_ref = db.collection('notes').document(note_id)
        note_doc = note_ref.get()
        
        if not note_doc.exists:
            return jsonify({'error': 'Note not found'}), 404
        
        note_data = note_doc.to_dict()
        if note_data.get('uid') != uid:
            return jsonify({'error': 'Unauthorized'}), 403
        
        note_ref.delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

