


variable "sec_name" {
  type = string
}

variable "sec_email" {
  type      = string
  sensitive = true
}

variable "pg_user" {
  type = string
  default = null
  nullable = true
}

variable "pg_password" {
  type      = string
  sensitive = true
  default = null
  nullable = true
}

variable "pg_host" {
  type = string
  default = null
  nullable = true
}