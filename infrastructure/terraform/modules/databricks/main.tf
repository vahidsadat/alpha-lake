resource "databricks_job" "alphalake" {
  name = var.name

  # schedule {
  #   quartz_cron_expression = "0 0 7 * * ?"
  #   timezone_id            = "Europe/Berlin"
  #   pause_status           = "UNPAUSED"
  # }

  environment {
    environment_key = "default"

    spec {
      environment_version = "6"
      dependencies = [
        "edgartools"
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
    notebook_task {
      notebook_path = var.notebook
      source        = "GIT"
      base_parameters = {
        sec_name  = var.sec_name,
        sec_email = var.sec_email
        ticker = var.ticker
      }
    }
  }

}