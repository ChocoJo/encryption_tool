import os
import logging
import argparse
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s'
)