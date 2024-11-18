import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey, ThroughputProperties, exceptions

# Load environment variables from .env file
load_dotenv()
connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
database_name = os.getenv('COSMOS_DB_DATABASE')
container_name = os.getenv('COSMOS_DB_CONTAINER')

if not connection_string:
    raise ValueError("COSMOS_DB_CONNECTION_STRING is not set in the .env file.")

# Initialize Cosmos Client
client = CosmosClient.from_connection_string(connection_string)

def main():
    try:
        # Create database if it does not exist
        database = client.create_database_if_not_exists(id=database_name)
        print(f"Database '{database_name}' is ready.")

        # Create container if it does not exist
        container = database.create_container_if_not_exists(
            id=container_name,
            partition_key=PartitionKey(path="/categoryId"),
            offer_throughput=ThroughputProperties(auto_scale_max_throughput=1000)
        )
        print(f"Container '{container_name}' is ready.")

        # Insert a sample item
        item = {
            'id': 'item1',
            'name': 'Road Bike 3000',
            'description': 'This is a very fast road bike.',
            'categoryId': 'bikes'
        }
        container.create_item(body=item)
        print(f"Item created: {item['id']}")

    except exceptions.CosmosHttpResponseError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
