module "eks" {
  source       = "../../modules/aws-eks"
  cluster_name = "trendlab-prd"
  environment  = "prd"
}
