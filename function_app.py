import azure.functions as func
import logging
from azure.cosmos.aio import CosmosClient
import os

#database_id = "webstats"
#container_id = "statsonload"

#original DB (lines 10 - 11)
database_name = "webstats"
container_name = "NumberOfWebViews"
#New DB (lines 13 - 14)
#database_name = "SampleDB"
#container_name = "SampleContainer"

#partition_key = "1"
#row_id = '1'

url = os.environ["DB_ACCOUNT_URL"]
key = os.environ["DB_ACCOUNT_KEY"]


client = CosmosClient(url, key)
#client = CosmosClient(url, credential=key)

# Set the total throughput (RU/s) for the database and container
# database_throughput = 1000

database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger2")
async def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('1: Python HTTP trigger function processed a request.')
    
    item = await container.read_item("1", partition_key="/id")
    #item = client.read_item(item=row_id)
    #Alternate attempts commented out
    #item = await container.read_item("1", partition_key="75BF1ACB-168D-469C-9AA3-1FD26BB4EA4C")
    #item = container.read_item("VisitCount")
    logging.info("2: hello")
    logging.info(item)
    item += 1

    updated_item = await container.upsert_item(item)

    return func.HttpResponse(
        f"Updated number of visitors: {updated_item} ",
        status_code=200
    )
        