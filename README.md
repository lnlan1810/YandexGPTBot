# YandexGPTBot
Telegram бо́т помогает подготовить ответ на экзаменационный вопрос по дисциплине «Операционные системы».

## Ссылку видеофайл с записью разворачивания бота и его тестирования.

[Видео с записью разворачивания и тестирования бота](https://disk.yandex.ru/i/KO0Ztfj8H0ndGw)

### Инструкция по работе с YandexGPT API

#### 1. Описание API

YandexGPT API предоставляет возможность взаимодействовать с моделью GPT для генерации текстов на основе заданных сообщений. API поддерживает несколько языков и ролей сообщений (например, системное сообщение, пользовательское сообщение).

---

#### 2. Основные параметры запроса

Для работы с API необходимо выполнить POST-запрос на URL:  
**`https://llm.api.cloud.yandex.net/foundationModels/v1/completion`**

##### **Обязательные заголовки:**
- `Accept: application/json`
- `Authorization: Bearer <IAM_TOKEN>`

##### **Тело запроса:**
Тело запроса представляет собой JSON-объект со следующей структурой:  

```json
{
  "modelUri": "gpt://<FOLDER_ID>/yandexgpt",
  "messages": [
    {
      "role": "system",
      "text": "Инструкция для модели или контекст выполнения запроса."
    },
    {
      "role": "user",
      "text": "Вопрос пользователя или текст запроса."
    }
  ]
}
```

**Описание полей:**
- `modelUri`: URI модели GPT. Указывается в формате `gpt://<FOLDER_ID>/yandexgpt`, где `<FOLDER_ID>` — идентификатор каталога в Yandex Cloud.
- `messages`: Список сообщений, передаваемых модели.  
  - `role`: Роль сообщения. Возможные значения:
    - `system`: системное сообщение с контекстом или инструкцией.
    - `user`: запрос от пользователя.  
  - `text`: текст сообщения.

---

#### 3. Пример запроса

```bash
curl -X POST "https://llm.api.cloud.yandex.net/foundationModels/v1/completion" \
-H "Accept: application/json" \
-H "Authorization: Bearer YOUR_IAM_TOKEN" \
-d '{
  "modelUri": "gpt://your-folder-id/yandexgpt",
  "messages": [
    {
      "role": "system",
      "text": "Вы — помощник, отвечающий на вопросы по операционным системам."
    },
    {
      "role": "user",
      "text": "Объясните разницу между процессами и потоками."
    }
  ]
}'
```

---

#### 4. Получение ответа

В случае успешного выполнения запроса, API возвращает JSON-объект следующего вида:

```json
{
  "result": {
    "alternatives": [
      {
        "status": "ALTERNATIVE_STATUS_FINAL",
        "message": {
          "text": "Процессы — это независимые единицы выполнения с собственным адресным пространством, в то время как потоки разделяют адресное пространство процесса и ресурсы."
        }
      }
    ]
  }
}
```


