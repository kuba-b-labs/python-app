from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.cosmos import CosmosClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()

#login via Service Principal
service_principal = ClientSecretCredential(
    tenant_id= getenv("tenant_id"),
    client_id= getenv("client_id"),
    client_secret= getenv("client_secret")
)
url = getenv("COSMOS_DB_URL")
db_service_principal = CosmosClient(url, service_principal)


# cosmos_db = CosmosClient(getenv("COSMOS_DB_URL"),getenv("COSMOS_DB_KEY"))

# cosmos_db_database = cosmos_db.get_database_client("test_database")

# cosmos_db_container = cosmos_db_database.get_container_client("test_container")



# entry = (
#     {
#         "id" : "1",
#         "dayId" : "21/07/2025",
#         "daily_intake" : "2000"
#     }
# )
# #cosmos_db_container.create_item(entry)

# #cosmos_db_container.delete_item("1",partition_key="21/07/2025")

# cosmos_db_container.upsert_item(entry)