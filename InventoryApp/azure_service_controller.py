from io import BytesIO
from RestronovaRMS import settings
from azure.storage.blob import BlobServiceClient, BlobClient

class BlobClientCreationError(Exception):
    pass

class FileUploadError(Exception):
    pass

def create_blob_service_client():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
        return blob_service_client
    except Exception as create_blob_service_error:
        raise BlobClientCreationError(f"Error creating Blob service client: {create_blob_service_error}")

def create_blob_client(blob_service_client: BlobServiceClient, file_name, container_name):
    try:
        container_client = blob_service_client.get_container_client(container_name)
        if not container_client.exists():
            container_client.create_container(public_access='blob') 

        blob_client = container_client.get_blob_client(file_name)
        return blob_client
    except Exception as create_blob_error:
        raise BlobClientCreationError(f"Error creating Blob client: {create_blob_error}")

def blob_exists(blob_client: BlobClient) -> bool:
    try:
        blob_client.get_blob_properties()
        return True
    except Exception as blob_not_found_error:
        return False

def delete_blob(blob_client: BlobClient):
    if blob_exists(blob_client):
        blob_client.delete_blob()

def upload_file_to_blob(file, container_name, blob_name):
    try:
        file_content = file.read()
        file_io = BytesIO(file_content)

        blob_service_client = create_blob_service_client()
        blob_client = create_blob_client(blob_service_client, file_name=blob_name, container_name=container_name)

        delete_blob(blob_client)

        blob_client.upload_blob(data=file_io)

        return blob_client.url

    except Exception as upload_error:
        raise FileUploadError(f"Error uploading file to blob: {upload_error}")
