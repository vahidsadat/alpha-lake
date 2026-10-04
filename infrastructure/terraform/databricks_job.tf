variable "ALPHALAKE_ENV" {
  type    = string
  default = "databricks"
}

variable "name" {
  type    = string
}

variable "email" {
  type      = string
  sensitive = true
}

locals {
  repo_base_path = "${data.databricks_current_user.me.home}/alpha-lake"
}
resource "databricks_job" "alphalake" {
    name = "AlphaLake Financial Pipeline"

    parameter {
      name  = "ALPHALAKE_ENV"
      default = var.ALPHALAKE_ENV
    }

    task {
      task_key = "01_bronze_ingestion"

      notebook_task {
        notebook_path = "${local.repo_base_path}/src/bronze/load_financials"

        base_parameters = {
          name          = var.name
          email         = var.email
        }
      }
    }

    task {
      task_key = "02_silver_transform"

      depends_on {
        task_key = "01_bronze_ingestion"
      }
      notebook_task {
        notebook_path = "${local.repo_base_path}/src/infrastructure/storage/databricks"
      }
    }

    task {
      task_key = "03_gold_transform"
      depends_on {
        task_key = "02_silver_transform"
      }
      notebook_task {
        notebook_path = "${local.repo_base_path}/AlphaLakeFinancialPipeline"
      }
    }

}
