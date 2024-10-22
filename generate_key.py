import os
import sys
import logging
from cryptography.fernet import Fernet
import argparse

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)