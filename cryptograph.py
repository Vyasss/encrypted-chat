from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import bcrypt

# Step 1: Symmetric Key Generation (AES-256 key)
key = os.urandom(32)
iv = os.urandom(16)

# AES encryption
def encrypt_message(message, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode('utf-8')) + encryptor.finalize()
    return ciphertext

# AES decryption
def decrypt_message(ciphertext, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message.decode('utf-8')

# bcrypt hashing
def hash_message(message):
    salt = bcrypt.gensalt()
    hashed_message = bcrypt.hashpw(message.encode('utf-8'), salt)
    return hashed_message

# bcrypt verification
def verify_message(message, hashed_message):
    return bcrypt.checkpw(message.encode('utf-8'), hashed_message)

# Example usage
message = "Hello, this is a secure message"

# Encrypt message with AES
encrypted_message = encrypt_message(message, key, iv)
print(f"Encrypted Message -> {encrypted_message.hex()}")

# Hash the original message using bcrypt
hashed_message = hash_message(message)
print(f"Hashed Message -> {hashed_message}")

# Decrypt the AES encrypted message
decrypted_message = decrypt_message(encrypted_message, key, iv)
print(f"Decrypted Message -> {decrypted_message}")

# Verify the original message against the hash
is_valid = verify_message(decrypted_message, hashed_message)
print(f"Is the message valid? -> {is_valid}")
