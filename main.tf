terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
    telegram = {
      source  = "yi-jiayu/telegram"
      version = "0.3.1"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = "ru-central1-a"
  service_account_key_file = var.sa_key_file_path
}

provider "telegram" {
  bot_token = var.tg_bot_key
}

resource "yandex_function" "tg_bot_for_exam" {
  name               = "echo2"
  entrypoint         = "index.handler"
  memory             = "128"
  runtime            = "python312"
  service_account_id = yandex_iam_service_account.tg_bot_for_exam.id
  user_hash          = data.archive_file.bot_function_zip.output_sha512
  execution_timeout  = "45"
  
  environment = {
    TELEGRAM_BOT_TOKEN = var.tg_bot_key
    FOLDER_ID          = var.folder_id
    MOUNT_POINT        = var.bucket_name
    BUCKET_OBJECT_KEY  = var.bucket_object_key
  }

  content {
    zip_filename = data.archive_file.bot_function_zip.output_path
  }

  mounts {
    name = var.bucket_name
    mode = "ro"
    object_storage {
      bucket = yandex_storage_bucket.tg_bot_for_exam_bucket.bucket
    }
  }
}

resource "yandex_function_iam_binding" "tg_bot_for_exam_iam" {
  function_id = yandex_function.tg_bot_for_exam.id
  role        = "functions.functionInvoker"
  members     = ["system:allUsers"]
}

resource "telegram_bot_webhook" "tg_bot_for_exam_webhook" {
  url = "https://functions.yandexcloud.net/${yandex_function.tg_bot_for_exam.id}"
}

resource "yandex_storage_bucket" "tg_bot_for_exam_bucket" {
  bucket = var.bucket_name
}

resource "yandex_storage_object" "yandexgpt_instruction" {
  bucket = yandex_storage_bucket.tg_bot_for_exam_bucket.id
  key    = var.bucket_object_key
  source = "instruction.txt"
}

resource "yandex_iam_service_account" "tg_bot_for_exam" {
  name = "tg-bot-for-exam"
}

resource "yandex_resourcemanager_folder_iam_member" "tg_bot_for_exam_ai_vision_iam" {
  folder_id = var.folder_id
  role      = "ai.vision.user"
  member    = "serviceAccount:${yandex_iam_service_account.tg_bot_for_exam.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "tg_bot_for_exam_ai_language_models_iam" {
  folder_id = var.folder_id
  role      = "ai.languageModels.user"
  member    = "serviceAccount:${yandex_iam_service_account.tg_bot_for_exam.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "tg_bot_for_exam_storage_viewer_iam" {
  folder_id = var.folder_id
  role      = "storage.viewer"
  member    = "serviceAccount:${yandex_iam_service_account.tg_bot_for_exam.id}"
}

variable "cloud_id" {
  type        = string
  description = "Cloud ID used for the Yandex provider"
}

variable "folder_id" {
  type        = string
  description = "Folder ID used for the Yandex resources"
}

variable "sa_key_file_path" {
  type        = string
  description = "Path to the service account key file with admin role"
  default     = "/Users/laptoptt/yc-keys/key.json"
}

variable "tg_bot_key" {
  type        = string
  description = "Telegram Bot API token"
}

variable "bucket_name" {
  type        = string
  description = "Name of the storage bucket containing instructions for YandexGPT"
  default     = "bucket035"
}

variable "bucket_object_key" {
  type        = string
  description = "Object key for the instruction file in the bucket"
  default     = "instruction.txt"
}

data "archive_file" "bot_function_zip" {
  type        = "zip"
  source_dir  = "src"
  output_path = "bot_function.zip"
}
