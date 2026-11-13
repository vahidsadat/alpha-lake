

variable "git_url" {
  type = string
}

variable "git_branch" {
  type = string
}

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

variable "ticker" {
  type = string
  default = null
  nullable = true
}

variable "schedule" {
  type = string
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