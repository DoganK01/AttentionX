from azure.storage.blob import BlobServiceClient
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from docker import from_env
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

client_id = os.environ['AZURE_CLIENT_ID']
tenant_id = os.environ['AZURE_TENANT_ID']
client_secret = os.environ['AZURE_CLIENT_SECRET']
vault_url = os.environ["AZURE_VAULT_URL"]

def upload_model_to_blob(storage_account_name, storage_account_key, container_name, model_folder_path = "/content/model_file"):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net/",
        credential=storage_account_key
    )
    container_client = blob_service_client.get_container_client(container_name)
    for root, _, files in os.walk(model_folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            with open(file_path, "rb") as model_file:
                # Use the relative path inside the folder as the blob name
                relative_path = os.path.relpath(file_path, model_folder_path)
                blob_name = relative_path.replace("\\", "/")  # Convert Windows path separators to Unix-style
                container_client.upload_blob(blob_name, model_file)
    print(f"Model uploaded to Blob Storage: {blob_name}")

def store_secret_in_keyvault(vault_url, secret_name, secret_value):
    credentials = ClientSecretCredential(client_id = client_id, client_secret= client_secret, tenant_id= tenant_id)
    client = SecretClient(vault_url=vault_url, credential=credential)
    client.set_secret(secret_name, secret_value)
    print(f"Secret stored in Key Vault: {secret_name}")



def push_docker_image_to_acr(subscription_id, resource_group, acr_name, image_name, dockerfile_path):
    docker_client = from_env()
    image, build_logs = docker_client.images.build(path=dockerfile_path, tag=image_name)

    credentials = ClientSecretCredential(client_id = client_id, client_secret= client_secret, tenant_id= tenant_id)
    acr_client = ContainerRegistryManagementClient(credential, subscription_id)
    acr_login_server = acr_client.registries.get(resource_group, acr_name).login_server
    docker_client.login(username="00000000-0000-0000-0000-000000000000",  # Service Principal ID
                        password="service_principal_password",  # Replace with secret from Key Vault
                        registry=acr_login_server)
    docker_client.images.push(repository=f"{acr_login_server}/{image_name}")

def query_logs(log_workspace_id, query):
    credentials = ClientSecretCredential(client_id = client_id, client_secret= client_secret, tenant_id= tenant_id)
    logs_client = LogsQueryClient(credential)

    response = logs_client.query_workspace(
        workspace_id=log_workspace_id,
        query=query,
        timespan=("PT1H", "PT0H")
    )
    for table in response.tables:
        for row in table.rows:
            print(row)



