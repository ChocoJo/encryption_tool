import os
import sys
import logging
from cryptography.fernet import Fernet
import argparse

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_user_confirmation(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        if get_user_confirmation(f"The directory '{directory}' does not exist. Do you want to create it? (y/n): "):
            try:
                os.makedirs(directory)
                logging.info(f"Directory '{directory}' created.")
            except Exception as e:
                logging.error(f"Failed to create directory '{directory}': {e}")
                sys.exit(1)
        else:
            logging.info("Operation aborted by user. Directory not created.")
            sys.exit(0)

def generate_key(file_path='secret.key'):
    ensure_directory_exists(file_path)
 
    if os.path.exists(file_path):
        if not get_user_confirmation(f"File '{file_path}' already exists. Do you want to overwrite it? (y/n): "):
            logging.info("Operation aborted by user. Key not overwritten.")
            sys.exit(0)
 
    try:
        key = Fernet.generate_key()
        with open(file_path, 'wb') as key_file:
            key_file.write(key)
        logging.info(f"Encryption key generated and saved to '{file_path}'")
    except PermissionError:
        logging.error(f"Permission denied: Unable to write to '{file_path}'. Please check your file permissions.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to write key to file {file_path}: {e}")
        sys.exit(1)