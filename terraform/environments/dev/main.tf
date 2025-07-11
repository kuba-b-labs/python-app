module "resource_group" {
  source          = "../../modules/resource_group"
  name            = var.name
  location        = var.location
  tags            = var.tags
  subscription_id = var.subscription_id
}

module "storage_account" {
  for_each = var.storage_accounts

  source   = "../../modules/storage_account"
  name     = each.value.name
  rg_name  = module.resource_group.name
  location = module.resource_group.location
  tags = {
    location = module.resource_group.location
  }
}
module "keyVault" {
  source    = "../../modules/keyVault"
  KV_name   = var.KV_name
  rg_name   = module.resource_group.name
  tags      = var.tags
  sku       = var.sku
  location  = module.resource_group.location
  tenant_id = var.tenant_id
}

data "azurerm_key_vault" "example" {
  name                = module.keyVault.name
  resource_group_name = module.resource_group.name
}

data "azurerm_key_vault_secret" "secret1" {
  name         = "test"
  key_vault_id = data.azurerm_key_vault.example.id
}
module "storage_account_test" {
  source   = "../../modules/storage_account"
  name     = "test104jbaz"
  rg_name  = "homelab"
  location = module.resource_group.location
  tags = {
    location   = module.resource_group.location
    production = data.azurerm_key_vault_secret.secret1.value
  }
}

#VM
module "linux_vm" {
  
  source              = "../../modules/virtual machines"
  rg_name             = var.vm_name
  admin_username = var.admin_username
  location = module.resource_group.location
  public_key = file("id_rsa.pub")
  vm_name = var.vm_name
  size = var.size
  nic_id = module.vnet.network_interface_ids
  depends_on = [ module.vnet ]
}

#vnet
module "vnet" {
  source = "../../modules/vnet"
  location = module.resource_group.location
  nic_name = var.nic_name
  rg_name = module.resource_group.name
  vnet_name = var.vnet_name
  subnet_name = var.subnet_name
}