from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives import hashes
import os
import json
import joblib  # For loading the phishing detection model
from flask_cors import CORS  # Import Flask-CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Symmetric Key Generation (AES-256 key)
key = os.urandom(32)
database_file = 'database.json'

# Load phishing model and vectorizer
model = joblib.load('phishing_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Helper function to load messages from the database.json file
def load_messages():
    if os.path.exists(database_file):
        with open(database_file, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # Handle if the file is empty or corrupted
                return {'user1': [], 'user2': []}
    else:
        # If the file doesn't exist, create a new structure
        return {'user1': [], 'user2': []}

# Helper function to save messages to the database.json file
def save_messages(messages):
    with open(database_file, 'w') as file:
        json.dump(messages, file, indent=4)

# Phishing Detection Function
def classify_message(message):
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)
    return "unsafe" if prediction[0] == 1 else "safe"

# Encrypt a message using AES and generate a new IV per message
def encrypt_message(message, key):
    iv = os.urandom(16)  # Generate a new IV for each message
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return iv + ciphertext  # Prepend the IV to the ciphertext

# Decrypt a message using AES
def decrypt_message(ciphertext, key):
    iv = ciphertext[:16]  # Extract the IV from the first 16 bytes
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    return decrypted_message.decode('utf-8')

# HMAC signing for integrity
def hmac_sign(key, message):
    hmac = HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac.update(message)
    return hmac.finalize()

# HMAC verification
def hmac_verify(key, message, signature):
    hmac = HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac.update(message)
    try:
        hmac.verify(signature)
        return True
    except:
        return False

# Route for user1 to send a message
@app.route('/send_message_user1', methods=['POST'])
def send_message_user1():
    data = request.json
    message = data['message']

    # Phishing Detection
    if classify_message(message) == "unsafe":
        return jsonify({'status': 'Message classified as unsafe. Not sent.'}), 400

    # Encrypt the message
    encrypted_message = encrypt_message(message, key)

    # Sign the encrypted message with HMAC for integrity
    signature = hmac_sign(key, encrypted_message)

    # Load messages from the JSON file
    messages = load_messages()

    # Add encrypted message, signature to user2's message queue with 'retrieved' flag as False
    messages['user2'].append({
        'encrypted_message': encrypted_message.hex(),
        'signature': signature.hex(),
        'retrieved': False
    })

    # Save the updated messages back to the JSON file
    save_messages(messages)

    return jsonify({'status': 'Message sent and encrypted!', 'encrypted_message': encrypted_message.hex()}), 200

# Route for user2 to send a message
@app.route('/send_message_user2', methods=['POST'])
def send_message_user2():
    data = request.json
    message = data['message']

    # Phishing Detection
    if classify_message(message) == "unsafe":
        return jsonify({'status': 'Message classified as unsafe. Not sent.'}), 400

    # Encrypt the message
    encrypted_message = encrypt_message(message, key)

    # Sign the encrypted message with HMAC for integrity
    signature = hmac_sign(key, encrypted_message)

    # Load messages from the JSON file
    messages = load_messages()

    # Add encrypted message, signature to user1's message queue with 'retrieved' flag as False
    messages['user1'].append({
        'encrypted_message': encrypted_message.hex(),
        'signature': signature.hex(),
        'retrieved': False
    })

    # Save the updated messages back to the JSON file
    save_messages(messages)

    return jsonify({'status': 'Message sent and encrypted!', 'encrypted_message': encrypted_message.hex()}), 200

# Route for user1 to receive messages
@app.route('/receive_messages_user1', methods=['GET'])
def receive_messages_user1():
    # Load messages from the JSON file
    messages = load_messages()
    user1_messages = messages['user1']
    decrypted_messages = []

    for msg in user1_messages:
        if not msg['retrieved']:
            # Convert back from hex to bytes
            encrypted_message = bytes.fromhex(msg['encrypted_message'])
            signature = bytes.fromhex(msg['signature'])

            # Verify the message integrity using HMAC
            if hmac_verify(key, encrypted_message, signature):
                decrypted_message = decrypt_message(encrypted_message, key)
                decrypted_messages.append(decrypted_message)
            else:
                decrypted_messages.append("Message integrity compromised!")

            # Mark message as retrieved
            msg['retrieved'] = True

    # Save the updated messages back to the JSON file
    save_messages(messages)

    return jsonify({'decrypted_messages': decrypted_messages}), 200

# Route for user2 to receive messages
@app.route('/receive_messages_user2', methods=['GET'])
def receive_messages_user2():
    # Load messages from the JSON file
    messages = load_messages()
    user2_messages = messages['user2']
    decrypted_messages = []

    for msg in user2_messages:
        if not msg['retrieved']:
            # Convert back from hex to bytes
            encrypted_message = bytes.fromhex(msg['encrypted_message'])
            signature = bytes.fromhex(msg['signature'])

            # Verify the message integrity using HMAC
            if hmac_verify(key, encrypted_message, signature):
                decrypted_message = decrypt_message(encrypted_message, key)
                decrypted_messages.append(decrypted_message)
            else:
                decrypted_messages.append("Message integrity compromised!")

            # Mark message as retrieved
            msg['retrieved'] = True

    # Save the updated messages back to the JSON file
    save_messages(messages)

    return jsonify({'decrypted_messages': decrypted_messages}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
