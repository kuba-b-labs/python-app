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



vm_name = "linux_vm"
admin_username = "test104"
size = "B1s"

#vnet
nic_name = "nic1" 
subnet_name = "sub1"
vnet_name = "vnet1"
