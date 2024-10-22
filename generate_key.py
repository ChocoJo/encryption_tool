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