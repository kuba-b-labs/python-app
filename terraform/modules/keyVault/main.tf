resource "azurerm_key_vault" "azkv1" {
  name                        = var.KV_name
  location                    = var.location
  resource_group_name         = var.rg_name
  enabled_for_disk_encryption = true
  tenant_id                   = var.tenant_id
  soft_delete_retention_days  = 7
  purge_protection_enabled    = false
  sku_name = var.sku
  enable_rbac_authorization = true
}