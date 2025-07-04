import logging
import os

# Define the log path
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, "logfile.log")

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_message(message: str):
    logging.info(message)

def log_error(error: str):
    logging.error(error)
