variable "name" {
  description = "Resource Group's name"
  type = string
}
variable "location" {
    description = "Resource Group's location"
    type = string
}
variable "tags" {
    description = "Resource Group's tags"
    type = map(string)
}
variable "subscription_id" {
  description = "Azure Subscription ID used in the provider block"
  type        = string
}
