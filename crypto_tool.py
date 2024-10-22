import os
import logging
import argparse
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_key(key_path):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
            if not key:
                raise ValueError("Key file is empty.")
            logging.info(f"Key successfully loaded from '{key_path}'")
            return key
    except FileNotFoundError:
        logging.error(f"Key file '{key_path}' not found.")
        exit(1)
    except ValueError as ve:
        logging.error(f"Error: {ve}")
        exit(1)
    except Exception as e:
        logging.error(f"Unexpected error while loading key: {e}")
        exit(1)

def handle_existing_file(file_path):
    if os.path.exists(file_path):
        confirmation = input(f"File '{file_path}' already exists. Do you want to overwrite? (y/n): ").strip().lower()
        if confirmation != 'y':
            logging.info("Operation aborted by the user.")
            exit(0)

def encrypt_file(file_path, key_path):
    if not os.path.exists(file_path):
        logging.error(f"File '{file_path}' not found.")
        exit(1)
 
    if file_path.endswith('.enc'):
        logging.error("File is already encrypted.")
        exit(1)
 
    key = load_key(key_path)
    fernet = Fernet(key)
 
    try:
        with open(file_path, 'rb') as file:
            original_data = file.read()
 
        encrypted_data = fernet.encrypt(original_data)
 
        output_file = f"{file_path}.enc"
        handle_existing_file(output_file)
 
        with open(output_file, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)
 
        logging.info(f"File '{file_path}' encrypted and saved as '{output_file}'.")
    except Exception as e:
        logging.error(f"Error during encryption: {e}")
        exit(1)

def decrypt_file(encrypted_file_path, key_path):
    if not encrypted_file_path.endswith('.enc'):
        logging.error("The file is not recognized as an encrypted file.")
        exit(1)
 
    if not os.path.exists(encrypted_file_path):
        logging.error(f"Encrypted file '{encrypted_file_path}' not found.")
        exit(1)

    key = load_key(key_path)
    fernet = Fernet(key)

    try:
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = fernet.decrypt(encrypted_data)
        original_file_path = encrypted_file_path.replace('.enc', '')
 

        if os.path.exists(original_file_path):
            while True:
                confirmation = input(f"File '{original_file_path}' already exists. Overwrite (o), Save as new (n), or Cancel (c)? ").strip().lower()
                if confirmation == 'o':
                    logging.info(f"Overwriting '{original_file_path}'.")
                    break
                elif confirmation == 'n':
                    original_file_path = input("Enter a new filename (without extension): ") + '.txt'
                    break
                elif confirmation == 'c':
                    logging.info("Operation aborted by the user.")
                    exit(0)
                else:
                    logging.warning("Invalid input. Please press 'o' to overwrite, 'n' to save as a new file, or 'c' to cancel.")
                    print("Invalid input. Please press 'o' to overwrite, 'n' to save as a new file, or 'c' to cancel.")
                   

        with open(original_file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        logging.info(f"File '{encrypted_file_path}' decrypted and saved as '{original_file_path}'.")
    except Exception as e:
        logging.error(f"Error during decryption: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files using a symmetric key.")
    parser.add_argument('mode', choices=['encrypt', 'decrypt'], help="Mode of operation: 'encrypt' or 'decrypt'")
    parser.add_argument('file', help="The file to encrypt or decrypt")
    parser.add_argument('--key', required=True, help="Path to the encryption key file")
 
    args = parser.parse_args()
 
    if args.mode == 'encrypt':
        encrypt_file(args.file, args.key)
    elif args.mode == 'decrypt':
        decrypt_file(args.file, args.key)
 
if __name__ == "__main__":
    main()