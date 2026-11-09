module "alphalake" {
    source = "./modules/databricks"
    sec_name = var.sec_name
    sec_email = var.sec_email
    notebook = var.notebook
    task_key = var.task_key
    name = var.name
}