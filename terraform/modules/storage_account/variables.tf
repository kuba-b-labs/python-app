variable "name"{
    description = "storage account name"
    type = string
}

variable "rg_name"{
    description = "storage account location"
    type = string
}

variable "location" {
    description = "storage account location"
    type = string

}

variable "account_tier"{
    description = "storage account tier"
    type = string
    default = "Standard"
}

variable "tags"{
    description = "storage account tags"
    type = map(string)
}
variable "account_replication_type" {
    description = "storage account replication type"
    default = "LRS"
    type = string
}
variable "access_tier" {
  description = "storage account access tier"
  default = "Cool"
}

