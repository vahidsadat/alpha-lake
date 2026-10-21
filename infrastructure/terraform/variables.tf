variable "ALPHALAKE_ENV" {
  type    = string
  default = "databricks"
}

variable "sec_name" {
  type = string
}

variable "sec_email" {
  type      = string
  sensitive = true
}

variable "repo_url" {
  type = string
}