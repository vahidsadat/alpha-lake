output "financial_pipeline_job_url" {
  description = "URL of the AlphaLake Financial Pipeline job"
  value       = module.financial_pipeline.job_url
}

output "financial_pipeline_job_id" {
  description = "ID of the AlphaLake Financial Pipeline job"
  value       = module.financial_pipeline.job_id
}

# --- Company sync job ---
output "company_sync_job_url" {
  description = "URL of the AlphaLake Get Companies Name job"
  value       = module.company_sync.job_url
}

output "company_sync_job_id" {
  description = "ID of the AlphaLake Get Companies Name job"
  value       = module.company_sync.job_id
}