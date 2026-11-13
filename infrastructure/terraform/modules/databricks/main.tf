resource "databricks_job" "alphalake" {
  name = var.name

  schedule {
    quartz_cron_expression = var.schedule
    timezone_id            = "Europe/Berlin"
    pause_status           = "UNPAUSED"
  }

  environment {
    environment_key = "default"

    spec {
      environment_version = "6"
      dependencies = [
        "edgartools",
         "sqlalchemy", 
         "python-dotenv", 
         "pg8000"
      ]
    }
  }
  git_source {
    url = var.git_url
    provider = "gitHub"
    branch = var.git_branch
  }

  task {
    task_key = var.task_key
    environment_key = "default"
    notebook_task {
      notebook_path = var.notebook
      source        = "GIT"
      base_parameters = {
        sec_name    = var.sec_name
        sec_email   = var.sec_email
        pg_user     = var.pg_user
        pg_password = var.pg_password
        pg_host     = var.pg_host
        ticker      = var.ticker
      }
    }
  }

}