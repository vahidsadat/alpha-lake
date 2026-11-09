variable "name" {
  type = string
}

variable "notebook" {
  type = string
}

variable "task_key" {
  type = string
}

variable "sec_name" {
  type = string
}

variable "sec_email" {
  type      = string
  sensitive = true
}
