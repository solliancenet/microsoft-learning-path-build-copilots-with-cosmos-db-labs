require('dotenv').config();
const { CosmosClient } = require('@azure/cosmos');

// Initialize Cosmos Client
const client = new CosmosClient(process.env.COSMOS_DB_CONNECTION_STRING);
const databaseId = process.env.COSMOS_DB_DATABASE;
const containerId = process.env.COSMOS_DB_CONTAINER;

async function main() {

    try {
        // Create database if it does not exist
        const { database } = await client.databases.createIfNotExists({ id: databaseId });
        console.log(`Database '${databaseId}' is ready.`);

        // Create container if it does not exist
        const { container } = await database.containers.createIfNotExists({
            id: containerId,
            partitionKey: { paths: ['/categoryId'] },
            maxThroughput: 1000,
        });
        console.log(`Container '${containerId}' is ready.`);

        // Insert a sample item
        const { resource: createdItem } = await container.items.create({
            id: 'item1',
            name: 'Road Bike 3000',
            description: 'This is a very fast road bike.',
            categoryId: 'bikes',
        });
        console.log(`Item created: ${createdItem.id}`);
    } catch (error) {
        console.error('Error:', error);
    }
}

main().catch(console.error);