module "aks" {
  source              = "../../modules/azure-aks"
  cluster_name        = "trendlab-hml"
  resource_group_name = "trendlab-hml-rg"
  environment         = "hml"
}
