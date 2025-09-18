# gemini_client.py
import google.generativeai as genai
from config import GEMINI_API_KEY, CAPTION_MODEL, EMBEDDING_MODEL

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

def generate_caption_and_details(image_path: str) -> str:
    """
    Sends an image to Gemini and asks for enriched caption + metadata.
    Returns JSON string in a clean, museum-style format.
    """
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        model = genai.GenerativeModel(CAPTION_MODEL)

        prompt = """
        You are describing archival images for a museum collection.
        Return ONLY valid JSON in this format:

        {
          "filename": "<image filename>",
          "caption": "<a short, natural one-sentence caption>",
          "detailed_description": "<a polished paragraph that provides historical, cultural, or contextual significance without being too literal. Aim for elegant, museum-style writing>",
          "tags": ["keyword1", "keyword2", "keyword3"],
          "contextual_category": "<one broad category (e.g. 'Historical Business Document', 'Postal History', 'Industrial Photography')>",
          "entities": {
            "people": ["list of people if identifiable"],
            "organizations": ["list of organizations mentioned or visible"],
            "locations": ["relevant places mentioned or inferred"],
            "date_estimate": "<approx date in human-readable form>"
          }
        }

        Guidelines:
        - Keep captions short (max 1 sentence).
        - Detailed descriptions should enrich context, not just restate what is visible.
        - Use neutral, historical, and professional tone (archival/museum style).
        - If unsure about details, leave them blank instead of guessing.
        - Ensure valid JSON only (no markdown, no comments).
        """

        response = model.generate_content(
            [prompt, {"mime_type": "image/jpeg", "data": image_bytes}]
        )

        return response.candidates[0].content.parts[0].text

    except Exception as e:
        return {"error": str(e)}


def generate_embeddings(text: str) -> list:
    """
    Generates embeddings for a given text using Gemini.
    """
    try:
        embedding = genai.embed_content(model=EMBEDDING_MODEL, content=text)
        return embedding["embedding"]
    except Exception as e:
        return {"error": str(e)}
