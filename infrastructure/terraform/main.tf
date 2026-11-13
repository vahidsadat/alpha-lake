module "financial_pipeline" {
  source      = "./modules/databricks"
  sec_name    = var.sec_name
  sec_email   = var.sec_email
  pg_user     = var.pg_user
  pg_password = var.pg_password
  pg_host     = var.pg_host
  notebook    = "src/notebooks/AlphaLakeFinancialPipeline"
  task_key    = "alphalake_pipeline"
  name        = "AlphaLake Financial Pipeline"
  ticker      = "AAPL, MSFT"
  git_branch  = "main"
  git_url     = "https://github.com/vahidsadat/alpha-lake"
  schedule    = "0 0 0 1 * ?"
}

module "company_sync" {
  source      = "./modules/databricks"
  sec_name    = var.sec_name
  sec_email   = var.sec_email
  pg_user     = var.pg_user
  pg_password = var.pg_password
  pg_host     = var.pg_host
  notebook    = "src/notebooks/GetCompaniesName"
  task_key    = "alphalake_get_company_info"
  name        = "AlphaLake Get Companies Name"
  git_branch  = "main"
  git_url     = "https://github.com/vahidsadat/alpha-lake"
  schedule    = "0 0 0 1 * ?"
}