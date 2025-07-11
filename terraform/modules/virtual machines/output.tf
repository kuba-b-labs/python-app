output "vm_id" {
  description = "The ID of the Virtual Machine"
  value       = azurerm_linux_virtual_machine.linux_vm.id
}

output "vm_name" {
  description = "The name of the Virtual Machine"
  value       = azurerm_linux_virtual_machine.linux_vm.name
}

output "vm_public_ip" {
  description = "Public IP address of the Virtual Machine"
  value       = azurerm_linux_virtual_machine.linux_vm.public_ip_address
  sensitive = true
}