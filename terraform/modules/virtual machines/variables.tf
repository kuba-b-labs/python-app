variable "vm_name" {
  type = string
}
variable "location" {
    type = string
}
variable "rg_name"{
    type = string
}
variable "size" {
    type = string
}
variable "admin_username"{
  type        = string
  sensitive = true
}
variable "public_key"{
  type        = string
}
variable "nic_id"{
  description = "Network Interface"
    type = string
}