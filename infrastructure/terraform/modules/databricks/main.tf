locals {
  repo_base_path = var.repo_base_path
}
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

  task {
    task_key = "alphalake_pipeline"
    notebook_task {
      notebook_path = "${local.repo_base_path}/${var.notebook}"
      source        = "WORKSPACE"
      base_parameters = {
        sec_name  = var.sec_name,
        sec_email = var.sec_email
      }
    }
  }

}