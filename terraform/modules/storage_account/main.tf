resource "azurerm_storage_account" "storage_account" {
  name                     = var.name
  resource_group_name      = var.rg_name
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.account_replication_type
  tags = var.tags
  access_tier = var.access_tier
}