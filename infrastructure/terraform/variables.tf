


variable "sec_name" {
  type = string
}

variable "sec_email" {
  type      = string
  sensitive = true
}

variable "pg_user" {
  type = string
}

variable "pg_password" {
  type      = string
  sensitive = true
}

variable "pg_host" {
  type = string
}