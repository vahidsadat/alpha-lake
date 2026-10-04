terraform {
  required_version = ">= 1.6.0"
  cloud {
    organization = "vahidsadat-org"

    workspaces {
      name = "alphalake"
    }
  }


  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = ">= 1.35.0"
    }
  }
}