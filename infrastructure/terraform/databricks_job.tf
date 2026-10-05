locals {
  repo_base_path = "/Workspace${data.databricks_current_user.me.home}/alpha-lake"
}
resource "databricks_job" "alphalake" {
  name = "AlphaLake Financial Pipeline"
  git_source {
    url      = var.repo_url
    provider = "gitHub"
    branch   = "main"

  }

  parameter {
    name    = "ALPHALAKE_ENV"
    default = var.ALPHALAKE_ENV
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
    task_key        = "01_bronze_ingestion"
    environment_key = "default"

    spark_python_task {
      python_file = "src/bronze/load_financials.py"
      source      = "GIT"
      parameters = [
        "--name", var.name,
        "--email", var.email
      ]
    }
  }


  task {
    task_key        = "02_silver_transform"
    environment_key = "default"

    depends_on {
      task_key = "01_bronze_ingestion"
    }
    spark_python_task {
      python_file = "src/infrastructure/storage/databricks.py"
      source      = "GIT"

    }
  }

  task {
    task_key = "03_gold_transform"
    depends_on {
      task_key = "02_silver_transform"
    }
    notebook_task {
      notebook_path = "${local.repo_base_path}/AlphaLakeFinancialPipeline"
      source        = "WORKSPACE"
    }
  }

}
