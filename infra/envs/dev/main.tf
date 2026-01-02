module "eks" {
  source       = "../../modules/aws-eks"
  cluster_name = "trendlab-dev"
  environment  = "dev"
}

# Example backend config (commented out)
# terraform {
#   backend "s3" {
#     bucket = "trendlab-tfstate"
#     key    = "dev/terraform.tfstate"
#     region = "us-east-1"
#   }
# }
