import requests
from config import YC_API_GPT_URL, FOLDER_ID, BUCKET_OBJECT_KEY, DEBUG
from utils import logger, get_object_from_bucket

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

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return None

    if DEBUG:
        logger.debug("GPT Response", data=response.json())

    alternatives = response.json()["result"]["alternatives"]
    answer = next(
        (alt["message"].get("text") for alt in alternatives if alt["status"] == "ALTERNATIVE_STATUS_FINAL"),
        None
    )

    return answer
