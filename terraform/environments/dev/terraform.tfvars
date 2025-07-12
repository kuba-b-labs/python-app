name     = "homelab"
location = "Poland Central"
tags = {
  location   = "Poland Central"
  production = "dev"
}
storage_name = "test"
storage_accounts = {
  "sa1" = {
    name = "kuba104b1"
  },
  "sa2" = {
    name = "kuba104b2"
  }
}

KV_name         = "kv1jb104"
sku             = "standard"



vm_name = "linuxvm"
admin_username = "test104"
size = "Standard_A1_v2"

#vnet
nic_name = "nic1" 
subnet_name = "sub1"
vnet_name = "vnet1"
