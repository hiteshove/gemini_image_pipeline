# processor.py
import os
import json
import re
from gemini_client import generate_caption_and_details, generate_embeddings
from utils import save_json, log_message

def clean_gemini_response(raw_response: str) -> str:
    """
    Removes Markdown fences like ```json ... ``` from Gemini output.
    """
    if isinstance(raw_response, str):
        # Remove triple backticks and 'json' labels
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", raw_response.strip())
        cleaned = re.sub(r"```$", "", cleaned.strip())
        return cleaned
    return raw_response

def process_image(image_path: str):
    """
    Full pipeline for one image:
    - Get caption & enriched metadata
    - Clean Gemini response
    - Enforce schema
    - Generate embeddings
    - Save as JSON
    """
    print(f"🔎 Processing {image_path}...")
    log_message(f"Processing {image_path}...")

    raw_response = generate_caption_and_details(image_path)
    cleaned_response = clean_gemini_response(raw_response)

    # Try parsing Gemini JSON
    try:
        enriched_data = json.loads(cleaned_response) if isinstance(cleaned_response, str) else cleaned_response
    except Exception as e:
        enriched_data = {"error": f"Failed to parse Gemini response: {str(e)}", "raw": raw_response}
        log_message(f"❌ JSON parsing failed for {image_path}")
        save_json(enriched_data, os.path.basename(image_path).replace(".jpg", ".json"))
        return

    # ✅ Enforce schema and polish
    final_data = {
        "filename": os.path.basename(image_path),
        "caption": enriched_data.get("caption", "").strip(),
        "detailed_description": enriched_data.get("detailed_description", "").strip(),
        "tags": sorted(set(enriched_data.get("tags", []))),  # remove duplicates
        "contextual_category": enriched_data.get("contextual_category", "").strip(),
        "entities": {
            "people": enriched_data.get("entities", {}).get("people", []),
            "organizations": enriched_data.get("entities", {}).get("organizations", []),
            "locations": enriched_data.get("entities", {}).get("locations", []),
            "date_estimate": enriched_data.get("entities", {}).get("date_estimate", "")
        }
    }

    # ✅ Generate embeddings
    caption = final_data["caption"]
    detailed_desc = final_data["detailed_description"]

    final_data["caption_embedding"] = generate_embeddings(caption)
    final_data["description_embedding"] = generate_embeddings(detailed_desc)

    # ✅ Save JSON per image
    filename = os.path.basename(image_path).replace(".jpg", ".json").replace(".JPG", ".json")
    save_json(final_data, filename)
    log_message(f"✅ Completed {image_path}")
