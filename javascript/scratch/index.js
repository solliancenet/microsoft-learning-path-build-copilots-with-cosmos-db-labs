require('dotenv').config();
const { CosmosClient, Database, Container } = require('@azure/cosmos');

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
        // await createItem(container);

        // Read the sample item
        await readItem(container, 'item1', 'bikes');

        // Read all items
        await readItems(container);

        // Read items with query
        await readItemsWithQuery(container);

        // Get database account details
        await getDatabaseAccountDetails();
    } catch (error) {
        console.error('Error:', error);
    }
}

async function createItem(container) {
    const { resource: createdItem } = await container.items.create({
        id: 'item1',
        name: 'Road Bike 3000',
        description: 'This is a very fast road bike.',
        categoryId: 'bikes',
    });
    console.log(`Item created: ${createdItem.id}`);
}

async function readItem(container, itemId, partitionKey) {
    const { resource: item } = await container.item(itemId, partitionKey).read();
    console.log(`Item read: ${item.id}`);
}

async function readItems(container) {
    const { resources: items } = await container.items.readAll().fetchAll();
    console.log('Reading items:');
    items.forEach(item => console.log(`Item: ${item.id}`));
}

async function readItemsWithQuery(container) {
    const querySpec = {
        query: 'SELECT * from c',
    };
    const { resources: items } = await container.items.query(querySpec).fetchAll();
    console.log('Reading items with query:');
    items.forEach(item => console.log(`Item: ${item.id}`));
}

async function getDatabaseAccountDetails() {
    let account = await client.getDatabaseAccount();
    console.log(`Account readable locations: ${account.resource.readableLocations.map(l => l.name).join(', ')}`);
}

main().catch(console.error);