import bcrypt

# Simulated user input
user_message = "mySecretMessage"

# Step 1: Generating a salt
salt = bcrypt.gensalt()
print(f"Step 1: Generated Salt -> {salt}")

# Step 2: Hashing the message with the salt
hashed_message = bcrypt.hashpw(user_message.encode('utf-8'), salt)
print(f"Step 2: Hashed Message (with Salt) -> {hashed_message}")

# Step 3: Verifying the hashed message (for comparison)
is_same = bcrypt.checkpw(user_message.encode('utf-8'), hashed_message)
print(f"Step 3: Is the original message the same? -> {is_same}")
