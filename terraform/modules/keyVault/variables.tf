variable "KV_name" {
  description = "KV's name"
  type = string
}
variable "location" {
    description = "KV's  location"
    type = string
}
variable "rg_name"{
    description = "storage account location"
    type = string
}
variable "tags" {
    description = "KV's  tags"
    type = map(string)
}
variable "tenant_id"{
  description = "Tenant ID"
  type        = string
}
variable "sku"{
    description = "KV sku"
    type = string
}