terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.23.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

# 1. Build the Data Lake (Google Cloud Storage Bucket)
resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  # This satisfies the strict GCP Organization Policy!
  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

# 2. Build the Data Warehouse (Google BigQuery Dataset)
resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

# 3. Build the Data Warehouse (Homework 3 Dataset)
resource "google_bigquery_dataset" "hw3_dataset" {
  dataset_id = var.hw3_bq_dataset_name
  location   = var.location
}