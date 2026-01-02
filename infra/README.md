# Infrastructure

This directory contains Terraform code to provision Kubernetes clusters on AWS (EKS) or Azure (AKS).

## Structure

- `modules/`: Reusable Terraform modules.
- `envs/`: Environment-specific configurations (dev, hml, prd).

## Usage

1.  **Select Environment**: `cd infra/envs/dev`
2.  **Initialize**: `terraform init`
3.  **Plan**: `terraform plan`
4.  **Apply**: `terraform apply`

## Backend Configuration

For production usage, uncomment and configure the backend block in each environment's `main.tf`.

- **AWS**: S3 Bucket + DynamoDB Table
- **Azure**: Storage Account Container
