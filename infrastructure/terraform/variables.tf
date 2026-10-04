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

variable "github_repo_url" {
  type = string
}