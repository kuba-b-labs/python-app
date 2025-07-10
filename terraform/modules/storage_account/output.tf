output "name" {
  value = azurerm_storage_account.storage_account.name
}
output "location" {
  value = azurerm_storage_account.storage_account.location
}
output "blob_connection_string" {
  value = azurerm_storage_account.storage_account.primary_blob_connection_string
}