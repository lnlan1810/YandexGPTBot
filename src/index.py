import json
import base64
import requests
from pathlib import Path
from os import getenv

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
FOLDER_ID = getenv("FOLDER_ID")
MOUNT_POINT = getenv("MOUNT_POINT")
BUCKET_OBJECT_KEY = getenv("BUCKET_OBJECT_KEY")

TELEGRAM_API_HOST = "https://api.telegram.org"
TELEGRAM_API_URL = f"{TELEGRAM_API_HOST}/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_URL = f"{TELEGRAM_API_HOST}/file/bot{TELEGRAM_BOT_TOKEN}"

YC_API_OCR_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"
YC_API_GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

DEBUG = getenv("DEBUG", True)


def handle_text_message(text, message, iam_token):
    answer = get_answer_from_gpt(text, iam_token)
    if not answer:
        send_message("Я не смог подготовить ответ на экзаменационный вопрос.", message)
        return

    send_message(answer, message)


def handle_photo_message(tg_photo, message, iam_token):

    image_id = tg_photo[-1]["file_id"]
    image_path = get_file_path(image_id)
    image = get_image(image_path)
    text = recognize_text(encode_to_base64(image), iam_token)
    if not text:
        send_message("Я не смог подготовить ответ на экзаменационный вопрос.", message)
        return

    handle_text_message(text, message, iam_token)
    

def handle_message(message, iam_token):
    if (text := message.get("text")) and text in {"/start", "/help"}:
        send_message(
            "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. "
            "Пришлите мне фотографию с вопросом или наберите его текстом.",
            message,
        )

    elif text := message.get("text"):
        handle_text_message(text, message, iam_token)

    elif image := message.get("photo"):
        handle_photo_message(image, message, iam_token)

    else:
        send_message("Я могу обработать только текстовое сообщение или фотографию.", message)


def handler(event, context):
    update = json.loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message, context.token["access_token"])

    return {
        "statusCode": 200,
    }


def encode_to_base64(bytes_content):
    return base64.b64encode(bytes_content).decode("utf-8")


class Logger:
    def log(self, level, message, data=None):
        message = {
            "level": level,
            "message": message,
        }

        if data:
            message["data"] = data

        print(json.dumps(message))

    def trace(self, message, data=None):
        return self.log(level="TRACE", message=message, data=data)

    def debug(self, message, data=None):
        return self.log(level="DEBUG", message=message, data=data)

    def info(self, message, data=None):
        return self.log(level="INFO", message=message, data=data)

    def warn(self, message, data=None):
        return self.log(level="WARN", message=message, data=data)

    def error(self, message, data=None):
        return self.log(level="ERROR", message=message, data=data)

    def fatal(self, message, data=None):
        return self.log(level="FATAL", message=message, data=data)


logger = Logger()


def send_message(reply_text, input_message):
    url = f"{TELEGRAM_API_URL}/sendMessage"

    data = {
        "chat_id": input_message["chat"]["id"],
        "text": reply_text,
        "reply_to_message_id": input_message["message_id"],
    }

    response = requests.post(url=url, json=data)
    if DEBUG:
        logger.debug(
            message=f"Message sent with status code {response.status_code}.",
            data=response.json(),
        )


def get_file_path(file_id):
    url = f"{TELEGRAM_API_URL}/getFile"

    data = {
        "file_id": file_id,
    }

    response = requests.get(url=url, params=data)
    if response.status_code != 200:
        return None

    return response.json()["result"].get("file_path")


def get_image(file_path):
    url = f"{TELEGRAM_FILE_URL}/{file_path}"

    response = requests.get(url=url)
    if response.status_code != 200:
        return None

    if DEBUG:
        logger.debug(
            message=f"Image received with status code {response.status_code}.",
        )

    return response.content


def get_answer_from_gpt(question, iam_token):
    url = YC_API_GPT_URL

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {iam_token}",
    }

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt",
        "messages": [
            {"role": "system", "text": get_object_from_bucket(BUCKET_OBJECT_KEY)},
            {"role": "user", "text": question},
        ],
    }

    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code != 200:
        return None

    if DEBUG:
        logger.debug(
            message=f"Message from GPT received with status code {response.status_code}.",
            data=response.json(),
        )

    alternatives = response.json()["result"]["alternatives"]
    final_alternatives = list(
        filter(
            lambda alternative: alternative["status"] == "ALTERNATIVE_STATUS_FINAL",
            alternatives,
        )
    )

    if not final_alternatives:
        return None

    answer = final_alternatives[0]["message"].get("text")
    return answer


def recognize_text(base64_image, iam_token):
    url = YC_API_OCR_URL

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token}",
    }

    data = {
        "content": base64_image,
        "mimeType": "image/jpeg",
        "languageCodes": ["ru", "en"],
    }

    response = requests.post(url=url, headers=headers, json=data)
    if response.status_code != 200:
        return None

    if DEBUG:
        logger.debug(
            message=f"Text from image was recognized with status code {response.status_code}.",
            data=response.json(),
        )

    text = response.json()["result"]["textAnnotation"]["fullText"]
    text = text.replace("-\n", "").replace("\n", " ")
    if not text:
        return None

    return text


def get_object_from_bucket(object_key):
    with open(Path("/function/storage", MOUNT_POINT, object_key), "r") as file:
        content = file.read()

    if DEBUG:
        logger.debug(
            message=f"Instruction from Object Storage received.",
            data={object_key: content},
        )

    return content
