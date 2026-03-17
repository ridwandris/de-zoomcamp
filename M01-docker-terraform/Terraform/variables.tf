variable "credentials" {
  description = "My Credentials"
  default     = "../../keys/my-creds.json"
}

variable "project" {
  description = "DTC DE Course Project ID"
  default     = "dtc-de-course-488907"
}

variable "region" {
  description = "Region for GCP resources"
  #Update the below to your desired region
  default = "europe-west1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default = "zoomcamp_dataset"
}

# New dataset for homework 3
variable "hw3_bq_dataset_name" {
  description = "BigQuery Dataset Name for Module 3 Homework"
  default     = "hw3_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "kestra-demo-bucket-ridwan99"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}