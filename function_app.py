import azure.functions as func
import logging
from azure.cosmos.aio import CosmosClient
import os

database_name = 'webcounter'
container_name = 'viewtracker'

item_id = '1'
partition_key_value = 'visitorCount'

url = os.environ['DB_ACCOUNT_URL']
key = os.environ['DB_ACCOUNT_KEY']

if not url or not key:
    raise ValueError('DB_ACCOUNT_URL and DB_ACCOUNT_KEY must be set in the environment variables.')

client = CosmosClient(url, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route='http_trigger2')
async def http_trigger2() -> func.HttpResponse:
    logging.info('1: Python HTTP trigger function processed a request.')

    # Read the item from the container
    item = await container.read_item(item_id, partition_key=partition_key_value)
    logging.info(f'2: {item}')

    # Increment the visitor count
    item['count'] += 1

    # Upsert the item back into the container
    updated_item = await container.upsert_item(item)

    return func.HttpResponse(
        f'Updated number of visitors: {updated_item['count']}',
        status_code=200
    )