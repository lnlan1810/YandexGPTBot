import json
import requests
from pathlib import Path
from config import TELEGRAM_API_URL, TELEGRAM_FILE_URL, DEBUG, MOUNT_POINT

class Logger:
    def log(self, level, message, data=None):
        log_message = {"level": level, "message": message, "data": data} if data else {"level": level, "message": message}
        print(json.dumps(log_message))

    def debug(self, message, data=None):
        if DEBUG:
            self.log("DEBUG", message, data)

logger = Logger()

def send_message(reply_text, input_message):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    data = {
        "chat_id": input_message["chat"]["id"],
        "text": reply_text,
        "reply_to_message_id": input_message["message_id"],
    }

    response = requests.post(url, json=data)
    if DEBUG:
        logger.debug("Message Sent", data=response.json())

def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile"
    response = requests.get(url, params={"file_id": file_id})
    return response.json().get("result", {}).get("file_path") if response.status_code == 200 else None

def get_image(file_path):
    url = f"{TELEGRAM_FILE_URL}/{file_path}"
    response = requests.get(url)
    return response.content if response.status_code == 200 else None

def get_object_from_bucket(object_key):
    with open(Path("/function/storage", MOUNT_POINT, object_key), "r") as file:
        content = file.read()
    
    if DEBUG:
        logger.debug("Bucket Object Retrieved", data={object_key: content})

    return content
