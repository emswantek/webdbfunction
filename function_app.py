import azure.functions as func
import logging
import asyncio
import uuid
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
from azure.cosmos.partition_key import PartitionKey

endpoint = "https://cloudresbackenddb.documents.azure.com:443/"
key = "DBKEY"

database_id = "webstats"
container_id = "statsonload"
partition_key = "/id"
row_id = '1'

# Set the total throughput (RU/s) for the database and container
database_throughput = 1000

# Singleton CosmosClient instance
client = CosmosClient(endpoint, credential=key)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
#Adding a test comment!
@app.route(route="http_trigger2")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    item = client.read_item(item=row_id)
    item['VisitCount'] += 1
    CosmosClient.upsert_item(item)

    return func.HttpResponse(
        f"Updated number of visitors: {item['VisitCount']} ",
        status_code=200
    )
        