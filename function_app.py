import azure.functions as func
import logging
import asyncio
import uuid
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
from azure.cosmos.partition_key import PartitionKey
import  os

endpoint = "https://cloudresbackenddb.documents.azure.com:443/"
key = "DBKEY"

url = os.environ["DB_ACCOUNT_URI"]
key = os.environ["DB_ACCOUNT_KEY"]
client = CosmosClient(url, key)

# Set the total throughput (RU/s) for the database and container
database_throughput = 1000

# Singleton CosmosClient instance
client = CosmosClient(endpoint, key)

# [START get_container]
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)
# [END get_container]

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
#Adding a test comment!
@app.route(route="http_trigger2")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    

    
    item = container.read_item("VisitCount", partition_key=[1])
    item['VisitCount'] += 1
    updated_item = container.upsert_item(item)

    return func.HttpResponse(
        f"Updated number of visitors: {item['VisitCount']} ",
        status_code=200
    )
        