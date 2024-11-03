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
    print("Loading messages from database...")
    if os.path.exists(database_file):
        with open(database_file, 'r') as file:
            try:
                messages = json.load(file)
                print("Messages loaded successfully.")
                return messages
            except json.JSONDecodeError:
                print("Error loading messages: File is empty or corrupted. Returning default structure.")
                return {'user1': [], 'user2': []}
    else:
        print("Database file not found. Creating new structure.")
        return {'user1': [], 'user2': []}

# Helper function to save messages to the database.json file
def save_messages(messages):
    print("Saving messages to database...")
    with open(database_file, 'w') as file:
        json.dump(messages, file, indent=4)
    print("Messages saved successfully.")

# Phishing Detection Function
def classify_message(message):
    print(f"Classifying message: {message}")
    vector = vectorizer.transform([message])
    prediction = model.predict(vector)
    classification = "unsafe" if prediction[0] == 1 else "safe"
    print(f"Message classification: {classification}")
    return classification

# Encrypt a message using AES and generate a new IV per message
def encrypt_message(message, key):
    print(f"Encrypting message: {message}")
    iv = os.urandom(16)  # Generate a new IV for each message
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    encrypted_message = iv + ciphertext  # Prepend the IV to the ciphertext
    print(f"Message encrypted: {encrypted_message.hex()}")
    return encrypted_message

# Decrypt a message using AES
def decrypt_message(ciphertext, key):
    print(f"Decrypting message: {ciphertext.hex()}")
    iv = ciphertext[:16]  # Extract the IV from the first 16 bytes
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    print(f"Message decrypted: {decrypted_message.decode('utf-8')}")
    return decrypted_message.decode('utf-8')

# HMAC signing for integrity
def hmac_sign(key, message):
    print("Signing message with HMAC...")
    hmac = HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac.update(message)
    signature = hmac.finalize()
    print(f"Message signed: {signature.hex()}")
    return signature

# HMAC verification
def hmac_verify(key, message, signature):
    print("Verifying HMAC signature...")
    hmac = HMAC(key, hashes.SHA256(), backend=default_backend())
    hmac.update(message)
    try:
        hmac.verify(signature)
        print("HMAC verification successful.")
        return True
    except:
        print("HMAC verification failed.")
        return False

# Route for user1 to send a message
@app.route('/send_message_user1', methods=['POST'])
def send_message_user1():
    data = request.json
    print(f"Received message from User 1: {data}")
    message = data['message']

    # Phishing Detection
    if classify_message(message) == "unsafe":
        print("Message classified as unsafe. Not sent.")
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

    print("Message from User 1 sent to User 2.")
    return jsonify({'status': 'Message sent and encrypted!', 'encrypted_message': encrypted_message.hex()}), 200

# Route for user2 to send a message
@app.route('/send_message_user2', methods=['POST'])
def send_message_user2():
    data = request.json
    print(f"Received message from User 2: {data}")
    message = data['message']

    # Phishing Detection
    if classify_message(message) == "unsafe":
        print("Message classified as unsafe. Not sent.")
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

    print("Message from User 2 sent to User 1.")
    return jsonify({'status': 'Message sent and encrypted!', 'encrypted_message': encrypted_message.hex()}), 200

# Route for user1 to receive messages
@app.route('/receive_messages_user1', methods=['GET'])
def receive_messages_user1():
    print("Retrieving messages for User 1...")
    messages = load_messages()
    user1_messages = messages['user1']
    decrypted_messages = []

    for msg in user1_messages:
        if not msg['retrieved']:
            encrypted_message = bytes.fromhex(msg['encrypted_message'])
            signature = bytes.fromhex(msg['signature'])

            # Verify the message integrity using HMAC
            if hmac_verify(key, encrypted_message, signature):
                decrypted_message = decrypt_message(encrypted_message, key)
                decrypted_messages.append(decrypted_message)
            else:
                decrypted_messages.append("Message integrity compromised!")

            msg['retrieved'] = True

    save_messages(messages)
    print(f"Messages retrieved for User 1: {decrypted_messages}")
    return jsonify({'decrypted_messages': decrypted_messages}), 200

# Route for user2 to receive messages
@app.route('/receive_messages_user2', methods=['GET'])
def receive_messages_user2():
    print("Retrieving messages for User 2...")
    messages = load_messages()
    user2_messages = messages['user2']
    decrypted_messages = []

    for msg in user2_messages:
        if not msg['retrieved']:
            encrypted_message = bytes.fromhex(msg['encrypted_message'])
            signature = bytes.fromhex(msg['signature'])

            # Verify the message integrity using HMAC
            if hmac_verify(key, encrypted_message, signature):
                decrypted_message = decrypt_message(encrypted_message, key)
                decrypted_messages.append(decrypted_message)
            else:
                decrypted_messages.append("Message integrity compromised!")

            msg['retrieved'] = True

    save_messages(messages)
    print(f"Messages retrieved for User 2: {decrypted_messages}")
    return jsonify({'decrypted_messages': decrypted_messages}), 200

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)  # Removed ssl_context
