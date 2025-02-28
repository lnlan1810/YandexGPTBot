import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
MOUNT_POINT = os.getenv("MOUNT_POINT")
BUCKET_OBJECT_KEY = os.getenv("BUCKET_OBJECT_KEY")

TELEGRAM_API_HOST = "https://api.telegram.org"
TELEGRAM_API_URL = f"{TELEGRAM_API_HOST}/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_URL = f"{TELEGRAM_API_HOST}/file/bot{TELEGRAM_BOT_TOKEN}"

YC_API_OCR_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
YC_API_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

DEBUG = os.getenv("DEBUG", True)
