locals {
  repo_base_path = "/Workspace${data.databricks_current_user.me.home}/alpha-lake"
}
resource "databricks_job" "alphalake" {
  name = "AlphaLake Financial Pipeline"

  # schedule {
  #   quartz_cron_expression = "0 0 7 * * ?"
  #   timezone_id            = "Europe/Berlin"
  #   pause_status           = "UNPAUSED"
  # }

  git_source {
    url      = var.repo_url
    provider = "gitHub"
    branch   = "main"
  }

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
      notebook_path = "${local.repo_base_path}/AlphaLakeFinancialPipeline"
      source        = "WORKSPACE"
      base_parameters = {
        sec_name  = var.sec_name,
        sec_email = var.sec_email
      }
    }
  }

}
