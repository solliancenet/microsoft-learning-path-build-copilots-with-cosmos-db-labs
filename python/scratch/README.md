# Azure Cosmos DB Python SDK - Python Quickstart

Steps to create the Python project:

1. Create and activate a virtual environment to manage dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

2. Install the Azure Cosmos DB Python SDK and `python-dotenv` for managing environment variables:

    ```bash
    pip install azure-cosmos python-dotenv
    ```

3. Freeze the installed packages into `requirements.txt`:

    ```bash
    pip freeze > requirements.txt
    ```

4. Create a `.env` file in the root of the project and add the following environment variables:

    ```bash
    COSMOS_DB_CONNECTION_STRING=<Your_Azure_Cosmos_DB_Connection_String>
    COSMOS_DB_DATABASE=<cosmosdb-database-name>
    COSMOS_DB_CONTAINER=<cosmosdb-container-name>
    ```

## Run the application

This project demonstrates how to use the Azure Cosmos DB Python SDK to interact with Cosmos DB.

### Setup

1. Clone this repository.
2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Run `pip install -r requirements.txt` to install dependencies.
4. Create a `.env` file with your Cosmos DB connection string:

    ```text
    COSMOS_DB_CONNECTION_STRING=<Your_Azure_Cosmos_DB_Connection_String>
    COSMOS_DB_DATABASE='cosmicworks'
    COSMOS_DB_CONTAINER='products'
    ```

### Running the Project

Run the following command to start the project:

```bash
python main.py
```
