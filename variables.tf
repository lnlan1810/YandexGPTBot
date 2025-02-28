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