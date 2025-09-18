# main.py
import glob
import os
from processor import process_image
from config import INPUT_DIR

def main():
    # Look for JPG images inside input/ folder
    image_files = glob.glob(os.path.join(INPUT_DIR, "*.jpg")) + glob.glob(os.path.join(INPUT_DIR, "*.JPG"))

    if not image_files:
        print("⚠️ No JPG images found in input/ directory.")
        return

    for img in image_files:
        process_image(img)

if __name__ == "__main__":
    main()
