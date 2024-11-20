import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey, ThroughputProperties, DatabaseProxy, ContainerProxy, ConsistencyLevel, exceptions

# Load environment variables from .env file
load_dotenv()
connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
database_name = os.getenv('COSMOS_DB_DATABASE')
container_name = os.getenv('COSMOS_DB_CONTAINER')

if not connection_string:
    raise ValueError("COSMOS_DB_CONNECTION_STRING is not set in the .env file.")

# Initialize Cosmos Client
client = CosmosClient.from_connection_string(
    connection_string,
    consistency_level=ConsistencyLevel.Eventual,
    preferred_locations=["West US", "East US"],
    connection_timeout=10)

def main():
    try:
        # Create database if it does not exist
        database = client.create_database_if_not_exists(id=database_name)
        print(f"Database '{database_name}' is ready.")

        database_instance = client.get_database_client(database_name)
        print(f"Database instance: {database_instance}")

        # Create container if it does not exist
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/categoryId"),
            offer_throughput=ThroughputProperties(auto_scale_max_throughput=1000)
        )
        print(f"Container '{container_name}' is ready.")

        container_instance = database.get_container_client(container_name)
        print(f"Container instance: {container_instance}")

        # Insert a sample item
        #create_item(container)

        # Read the sample item
        read_item(container, 'item1', 'bikes')

        # Read all items
        read_items(container)

        # Read items by query
        read_items_by_query(container)

        # Get database account details
        get_database_account_details()

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error: {e}")

def create_item(container: ContainerProxy):
    item = {
        'id': 'item1',
        'name': 'Road Bike 3000',
        'description': 'This is a very fast road bike.',
        'categoryId': 'bikes'
    }
    container.create_item(body=item)
    print(f"Item created: {item['id']}")

def read_item(container: ContainerProxy, item_id: str, partition_key: str):
    item = container.read_item(item=item_id, partition_key=partition_key)
    print(f"Item read: {item['id']}")

def read_items(container: ContainerProxy):
    items = list(container.read_all_items())
    print('Reading all items:')
    for item in items:
        print(f"Item: {item['id']}")

def read_items_by_query(container: ContainerProxy):
    query = "SELECT * FROM c WHERE c.categoryId = 'bikes'"
    items = list(container.query_items(query=query))
    print('Reading items by query:')
    for item in items:
        print(f"Item: {item['id']}")

def get_database_account_details():
    account = client.get_database_account()
    print(f"Account readable locations: {account.ReadableLocations}")

if __name__ == "__main__":
    main()
