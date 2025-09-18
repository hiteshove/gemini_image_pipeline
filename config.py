# config.py
import os

# Load Gemini API key from environment variable
# Set this before running: export GEMINI_API_KEY="your_api_key_here"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBS1ijFE1qkyXt6yyBH8rZswPlA6UsbJEI")

# Model names
CAPTION_MODEL = "gemini-2.5-flash"
EMBEDDING_MODEL = "text-embedding-004"

# Directories
INPUT_DIR = "input"
OUTPUT_DIR = "output"
