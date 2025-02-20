import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

# Function to encrypt a file
def encrypt_file(input_file: str, output_file: str, password: str):
    try:
        # Key derivation
        salt = get_random_bytes(16)
        key = PBKDF2(password, salt, dkLen=32, count=100000)

        # Encryption setup
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv

        # Read plaintext from the input file
        with open(input_file, "rb") as f:
            plaintext = f.read()

        # Encrypt and pad the plaintext
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        # Write salt, IV, and ciphertext to the output file
        with open(output_file, "wb") as f:
            f.write(salt + iv + ciphertext)

        print(f"File '{input_file}' encrypted and saved as '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error encrypting file: {e}")

# Function to decrypt a file
def decrypt_file(input_file: str, output_file: str, password: str):
    try:
        # Read salt, IV, and ciphertext from the input file
        with open(input_file, "rb") as f:
            data = f.read()

        salt = data[:16]
        iv = data[16:32]
        ciphertext = data[32:]

        # Key derivation
        key = PBKDF2(password, salt, dkLen=32, count=100000)

        # Decrypt setup
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt and remove padding
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # Write plaintext to the output file
        with open(output_file, "wb") as f:
            f.write(plaintext)

        print(f"File '{input_file}' decrypted and saved as '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error decrypting file: {e}")

# Main Execution
if __name__ == "__main__":
    # User-defined password
    password = "YourSecurePassword"

    # Encrypt the file
    encrypt_file("input.txt", "encrypted.bin", password)

    # Decrypt the file
    decrypt_file("encrypted.bin", "decrypted.txt", password)
