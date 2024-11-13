import azure.functions as func
import logging
from azure.cosmos.aio import CosmosClient
from azure.cosmos import exceptions
from azure.cosmos.partition_key import PartitionKey
import asyncio

endpoint = "https://cloudresbackenddb.documents.azure.com:443/"
key = "DBKEY"
database_id = "webstats"
container_id = "statsonload"
partition_key = "/VisitCount"
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
    
    name = req.params.get('name')
    item = container.read_item(item=row_id)
    item['VisitCount'] += 1
    container.upsert_item(item)
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        #return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(f"Updated number of visitors: {item['VisitCount']} ") 

    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
        