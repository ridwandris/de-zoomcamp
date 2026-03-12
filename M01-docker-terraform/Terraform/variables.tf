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
  default = "us-central1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default = "terraform-demo-terra-bucket-ridwan99"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}