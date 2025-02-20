import hashlib
import os
import json

user_data = {}

# Function to generate a salted SHA-256 hash3
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # Generate a 16-byte random salt
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()
    return salt.hex(), hashed_password

# Function to register a new user
def register():
    username = input("Enter username: ").strip()
    if username in user_data:
        print("Username already exists! Try a different username.")
        return

    password = input("Enter password: ").strip()
    salt, hashed_password = hash_password(password)
    user_data[username] = {"salt": salt, "password": hashed_password}

    save_data()
    print(f"User '{username}' registered successfully!")

# Function to authenticate a user
def login():
    username = input("Enter username: ").strip()
    if username not in user_data:
        print("Invalid username or password!")
        return

    password = input("Enter password: ").strip()
    salt = bytes.fromhex(user_data[username]["salt"])
    hashed_password = hashlib.sha256(salt + password.encode()).hexdigest()

    if hashed_password == user_data[username]["password"]:
        print("Login successful! ✅")
    else:
        print("Invalid username or password! ❌")

# Function to save user data to a file (persistent storage)
def save_data(file_path="users.json"):
    with open(file_path, "w") as f:
        json.dump(user_data, f)

# Function to load user data from a file
def load_data(file_path="users.json"):
    global user_data
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            user_data = json.load(f)

# Load previous user data (if available)
load_data()

while True:
    print("\n--- Secure Password Storage System ---")
    print("[1] Register  [2] Login  [3] Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        print("Exiting")
        break
    else:
        print("Please select either 1 or 2 or 3.")
