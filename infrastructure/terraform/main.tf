module "alphalake" {
  source         = "./modules/databricks"
  sec_name       = var.sec_name
  sec_email      = var.sec_email
  notebook       = var.notebook
  task_key       = var.task_key
  name           = var.name
  repo_base_path = "/Workspace${data.databricks_current_user.me.home}/alpha-lake"
}