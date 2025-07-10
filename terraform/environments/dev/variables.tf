variable "name" {
  description = "Resource Group's name"
  type        = string
}
variable "location" {
  description = "Resource Group's location"
  type        = string
}
variable "tags" {
  description = "Resource Group's tags"
  type        = map(string)
}
variable "subscription_id" {
  description = "Azure Subscription ID used in the provider block"
  type        = string
}
variable "storage_name" {
  description = "Storage Account Name"
  type = string
}

variable "storage_accounts" {
  description = "Storage accounts list"   
  type = map(object({
    name = string
  }))
}
variable "KV_name"{
  description = "KV's name"
  type = string
}
variable "tenant_id"{
  description = "Tenant ID"
  type        = string
}
variable "sku"{
    description = "KV sku"
    type = string
}
