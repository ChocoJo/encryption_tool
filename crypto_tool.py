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