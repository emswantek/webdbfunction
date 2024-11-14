import azure.functions as func
import logging
import asyncio
import uuid
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
from azure.cosmos.partition_key import PartitionKey
import os

database_id = "webstats"
container_id = "statsonload"

database_name = "webstats"
container_name = "NumberOfWebViews"

partition_key = "/id"
row_id = '1'

url = os.environ["DB_ACCOUNT_URL"]
key = os.environ["DB_ACCOUNT_KEY"]

client = CosmosClient(url, key)
#client = CosmosClient(url, credential=key)

# Set the total throughput (RU/s) for the database and container
database_throughput = 1000

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger2")
def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    #item = client.read_item(item=row_id)
    item = container.read_item("VisitCount", partition_key=[1])

    item += 1

    updated_item = container.upsert_item(item)

    return func.HttpResponse(
        f"Updated number of visitors: {updated_item} ",
        status_code=200
    )
        