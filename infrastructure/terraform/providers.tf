provider "databricks" {
}
data "databricks_current_user" "me" {}
data "databricks_spark_version" "latest" {}
# Query the smallest available compute node type
data "databricks_node_type" "smallest" {
  local_disk = true
}