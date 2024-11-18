# Azure Cosmos DB JavaScript SDK - Node.js Quickstart

Steps to create the NodeJS project:

1. Initialize a new Node.js project:

    ```bash
    npm init -y
    ```

2. Install the Azure Cosmos DB JavaScript SDK and `dotenv` (for securely managing environment variables) packages:

    ```bash
    npm install @azure/cosmos dotenv
    npm install dotenv --save
    ```

3. Create a `.env` file in the root of the project and add the following environment variables:

    ```bash
    COSMOS_DB_CONNECTION_STRING=<Your_Azure_Cosmos_DB_Connection_String>
    COSMOS_DB_DATABASE=<cosmosdb-database-name>
    COSMOS_DB_CONTAINER=<cosmosdb-container-name>
    ```

## Run the application

This project demonstrates how to use the Azure Cosmos DB JavaScript SDK to interact with Cosmos DB from a Node.js application.

### Setup

1. Clone this repository.
2. Run `npm install` to install dependencies.
3. Create a `.env` file with your Cosmos DB connection string:

    ```text
    COSMOS_DB_CONNECTION_STRING=<Your_Azure_Cosmos_DB_Connection_String>
    COSMOS_DB_DATABASE='cosmicworks'
    COSMOS_DB_CONTAINER='products'
    ```

### Running the Project

Run the following command to start the project:

```bash
npm start
```
