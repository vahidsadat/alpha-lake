variable "ALPHALAKE_ENV" {
  type    = string
  default = "databricks"
}

variable "name" {
  type = string
}

variable "email" {
  type      = string
  sensitive = true
}

variable "repo_url" {
  type = string
}