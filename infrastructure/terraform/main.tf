module "alphalake" {
  source     = "./modules/databricks"
  sec_name   = var.sec_name
  sec_email  = var.sec_email
  notebook   = var.notebook
  task_key   = var.task_key
  name       = var.name
  ticker     = var.ticker
  git_branch = "main"
  git_url    = "https://github.com/vahidsadat/alpha-lake"
}