output "financial_pipeline_job_url" {
  description = "URL of the AlphaLake Financial Pipeline job"
  value       = module.financial_pipeline.job_url
}

output "financial_pipeline_job_id" {
  description = "ID of the AlphaLake Financial Pipeline job"
  value       = module.financial_pipeline.job_id
}
