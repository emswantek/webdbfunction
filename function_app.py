import azure.functions as func
import logging
import json
from azure.cosmos.aio import CosmosClient
import os

database_name = "webcounter"
container_name = "viewtracker"
item_id = "1"
partition_key_value = "visitorCount"

url = os.environ["DB_ACCOUNT_URL"]
key = os.environ["DB_ACCOUNT_KEY"]


client = CosmosClient(url, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger2")
async def http_trigger2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('1: Python HTTP trigger function processed a request.')
    
    #item = client.read_item(item=row_id)
    item = await container.read_item("rownum", partition_key=1)
    #item = container.read_item("VisitCount")
    logging.info("2: hello")
    logging.info(item)
    item += 1

    updated_item = await container.upsert_item(item)

    return func.HttpResponse(
        f"Updated number of visitors: {updated_item} ",
        status_code=200
    )


@app.route(route="http_trigger3")
async def http_trigger3(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('1: Python HTTP trigger function processed a request.')
    jsondata = {
        "count": 0,
    }

    try:
        # Read the item from the container
        item = await container.read_item(item=item_id, partition_key=partition_key_value)
        logging.info(f"2: {item}")

        # Increment the visitor count
        item['count'] += 1

        # Upsert the item back into the container
        updated_item = await container.upsert_item(item)
        logging.info(f"Updated number of visitors: {updated_item['count']}"),
        jsondata.count = updated_item["count"]
        
    except Exception as e:
        logging.error(f"Error processing the request: {str(e)}")
        return func.HttpResponse(
            "An error occurred while processing your request.",
            status_code=500
        )

    return func.HttpResponse(
        #f"Updated number of visitors: {updated_item['count']}",
        #f"{jsondata}",
        f"{json.dumps(jsondata)}",
        status_code=200
    )
