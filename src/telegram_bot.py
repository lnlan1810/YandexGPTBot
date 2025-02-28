from utils import send_message, get_file_path, get_image
from ocr import recognize_text
from gpt import get_answer_from_gpt

def handle_text_message(text, message, iam_token):
    answer = get_answer_from_gpt(text, iam_token)
    if not answer:
        send_message("Я не смог подготовить ответ на экзаменационный вопрос.", message)
        return

    send_message(answer, message)

def handle_photo_message(tg_photo, message, iam_token):
    image_id = tg_photo[-1]["file_id"]
    image_path = get_file_path(image_id)
    
    if not image_path:
        send_message("Не удалось получить изображение.", message)
        return

    image = get_image(image_path)
    if not image:
        send_message("Ошибка загрузки изображения.", message)
        return

    text = recognize_text(image, iam_token)
    if not text:
        send_message("Не удалось распознать текст на изображении.", message)
        return

    handle_text_message(text, message, iam_token)

def handle_message(message, iam_token):
    text = message.get("text")

    if text in {"/start", "/help"}:
        send_message(
            "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. "
            "Пришлите мне фотографию с вопросом или наберите его текстом.",
            message
        )
    elif text:
        handle_text_message(text, message, iam_token)
    elif "photo" in message:
        handle_photo_message(message["photo"], message, iam_token)
    else:
        send_message("Я могу обработать только текстовое сообщение или фотографию.", message)
