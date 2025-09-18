# utils.py
import os
import json
from datetime import datetime
from config import OUTPUT_DIR

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_json(data: dict, filename: str):
    """
    Saves JSON data to output directory.
    """
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Saved: {path}")

def log_message(message: str):
    """
    Logs messages to a file for debugging.
    """
    ensure_output_dir()
    log_path = os.path.join(OUTPUT_DIR, "pipeline.log")
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.now().isoformat()}] {message}\n")
