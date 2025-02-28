import base64
import requests
from config import YC_API_OCR_URL, DEBUG
from utils import logger

def encode_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")

def recognize_text(image_bytes, iam_token):
    url = YC_API_OCR_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}",
    }

    data = {
        "content": encode_to_base64(image_bytes),
        "mimeType": "image/jpeg",
        "languageCodes": ["ru", "en"],
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return None

    text = response.json().get("result", {}).get("textAnnotation", {}).get("fullText", "").replace("-\n", "").replace("\n", " ")
    
    if DEBUG:
        logger.debug("OCR Response", data=response.json())

    return text if text else None
