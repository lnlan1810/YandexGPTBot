import json
from telegram_bot import handle_message
from config import DEBUG
from utils import logger

def handler(event, context):
    update = json.loads(event["body"])
    message = update.get("message")

    if message:
        handle_message(message, context.token["access_token"])

    if DEBUG:
        logger.debug("Event processed successfully", data=update)

    return {"statusCode": 200}
