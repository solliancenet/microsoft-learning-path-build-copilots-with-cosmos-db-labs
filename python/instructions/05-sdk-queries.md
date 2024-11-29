---
title: '05 - Execute a query with the Azure Cosmos DB for NoSQL SDK'
lab:
    title: '05 - Execute a query with the Azure Cosmos DB for NoSQL SDK'
    module: 'Query the Azure Cosmos DB for NoSQL'
layout: default
nav_order: 8
parent: 'Python SDK labs'
---

# Execute a query with the Azure Cosmos DB for NoSQL SDK

The latest version of the Python SDK for Azure Cosmos DB for NoSQL simplifies querying a container and iterating over result sets using Python's modern features.

The `azure-cosmos` library has built-in functionality to make querying Azure Cosmos DB efficient and straightforward.

In this lab, you'll use an iterator to process a large result set returned from Azure Cosmos DB for NoSQL. You will use the Python SDK to query and iterate over results.

## Prepare your development environment

If you have not already cloned the lab code repository for **Build copilots with Azure Cosmos DB** to the environment where you're working on this lab, follow these steps to do so. Otherwise, open the previously cloned folder in **Visual Studio Code**.

1. Start **Visual Studio Code**.

    > &#128221; If you are not already familiar with the Visual Studio Code interface, review the [Get Started guide for Visual Studio Code][code.visualstudio.com/docs/getstarted]

1. Open the command palette and run **Git: Clone** to clone the ``https://github.com/solliancenet/microsoft-learning-path-build-copilots-with-cosmos-db-labs`` GitHub repository in a local folder of your choice.

    > &#128161; You can use the **CTRL+SHIFT+P** keyboard shortcut to open the command palette.

1. Once the repository has been cloned, open the local folder you selected in **Visual Studio Code**.

## Create an Azure Cosmos DB for NoSQL account

Azure Cosmos DB is a cloud-based NoSQL database service that supports multiple APIs. When provisioning an Azure Cosmos DB account for the first time, you will select which of the APIs you want the account to support (for example, **Mongo API** or **NoSQL API**). Once the Azure Cosmos DB for NoSQL account is done provisioning, you can retrieve the endpoint and key and use them to connect to the Azure Cosmos DB for NoSQL account using the Azure SDK for Python or any other SDK of your choice.

1. In a new web browser window or tab, navigate to the Azure portal (``portal.azure.com``).

1. Sign into the portal using the Microsoft credentials associated with your subscription.

1. Select **+ Create a resource**, search for *Cosmos DB*, and then create a new **Azure Cosmos DB for NoSQL** account resource with the following settings, leaving all remaining settings to their default values:

    | **Setting** | **Value** |
    | ---: | :--- |
    | **Subscription** | *Your existing Azure subscription* |
    | **Resource group** | *Select an existing or create a new resource group* |
    | **Account Name** | *Enter a globally unique name* |
    | **Location** | *Choose any available region* |
    | **Capacity mode** | *Provisioned throughput* |
    | **Apply Free Tier Discount** | *Do Not Apply* |
    | **Limit the total amount of throughput that can be provisioned on this account** | *Unchecked* |

    > &#128221; Your lab environments may have restrictions preventing you from creating a new resource group. If that is the case, use the existing pre-created resource group.

1. Wait for the deployment task to complete before continuing with this task.

1. Go to the newly created **Azure Cosmos DB** account resource and navigate to the **Keys** pane.

1. This pane contains the connection details and credentials necessary to connect to the account from the SDK. Specifically:

    1. Notice the **URI** field. You will use this **endpoint** value later in this exercise.

    1. Notice the **PRIMARY KEY** field. You will use this **key** value later in this exercise.

## Create Azure Cosmos DB database and container with sample data

1. Within the newly created **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, select **Launch quick start** on the home page.

1. Within the **New Container** form, enter the following values:

    - **Database id**: `cosmicworks`
    - **Container id**: `products`
    - **Partition key**: `/categoryId`
    - **Container throughput (autoscale)**: Select `Autoscale`
    - **Container Max RU/s**: `1000`

1. Select **OK** to create the new container. This process will take a minute or two while it creates the resources and preloads the container with sample product data.

1. Keep the browser tab open, as we will return to it later.

1. Switch back to **Visual Studio Code**.

## Install the azure-cosmos library

The **azure-cosmos** library is available on **PyPI** for easy installation into your Python projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/05-sdk-queries** folder.

1. Open the context menu for the **python/05-sdk-queries** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **python/05-sdk-queries** folder.

1. Create and activate a virtual environment to manage dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

1. Install the [azure-cosmos][pypi.org/project/azure-cosmos] package using the following command:

    ```bash
    pip install azure-cosmos
    ```

## Iterate over the results of a SQL query using the SDK

Using the credentials from the newly created account, you will connect with the SDK classes and connect to the database and container you provisioned in an earlier step, and iterate over the results of a SQL query using the SDK.

You will now use an iterator to create a simple-to-understand loop over paginated results from Azure Cosmos DB. Behind the scenes, the SDK will manage the feed iterator and ensure subsequent requests are invoked correctly.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/05-sdk-queries** folder.

1. Open the blank Python file named **script.py**.

1. Add the following `import` statement to import the **CosmosClient** class:

    ```python
    from azure.cosmos import CosmosClient, PartitionKey
    ```

1. Add variables named **endpoint** and **key** and set their values to the **endpoint** and **key** of the Azure Cosmos DB account you created earlier.

    ```python
    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"
    ```

    > &#128221; For example, if your endpoint is: **https://dp420.documents.azure.com:443/**, the statement would be: **endpoint = "https://dp420.documents.azure.com:443/"**.

    > &#128221; If your key is: **fDR2ci9QgkdkvERTQ==**, the statement would be: **key = "fDR2ci9QgkdkvERTQ=="**.

1. Add a new variable named **client** and initialize it as a new instance of the **CosmosClient** class using the **endpoint** and **key** variables:

    ```python
    client = CosmosClient(endpoint, key)
    ```

1. Add the following code to connect to the database and container you created earlier:

    ```python
    database = client.get_database_client("cosmicworks")
    container = database.get_container_client("products")
    ```

1. Create a query string variable named `sql` with a value of `SELECT * FROM products p`.

    ```python
    sql = "SELECT * FROM products p"
    ```

1. Invoke the [`query_items`](https://learn.microsoft.com/python/api/azure-cosmos/azure.cosmos.container.containerproxy?view=azure-python#azure-cosmos-container-containerproxy-query-items) method with the `sql` variable as a parameter to the constructor. The `enable_cross_partition_query`, when set to `True`, allows sending of more than one request to execute the query in the Azure Cosmos DB service. More than one request is necessary if the query is not scoped to single partition key value.

    ```python
    result_iterator = container.query_items(
        query=sql,
        enable_cross_partition_query=True
    )
    ```

1. Iterate over the paginated results and print the `id`, `name`, and `price` of each item.

    ```python
    for item in result_iterator:
        print(f"[{item['id']}]	{item['name']}	${item['price']:.2f}")
    ```

1. Your **script.py** file should now look like this:

    ```python
    from azure.cosmos import CosmosClient, PartitionKey

    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"

    client = CosmosClient(endpoint, key)

    database = client.get_database_client("cosmicworks")
    container = database.get_container_client("products")
    
    sql = "SELECT * FROM products p"
    
    result_iterator = container.query_items(
        query=sql,
        enable_cross_partition_query=True
    )
    
    for item in result_iterator:
        print(f"[{item['id']}]	{item['name']}	${item['price']:.2f}")
    ```

1. **Save** the **script.py** file.

1. Run the script to create the database and container:

    ```bash
    python script.py
    ```

1. The script will now output every product in the container.

1. Close the integrated terminal.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[pypi.org/project/azure-cosmos]: https://pypi.org/project/azure-cosmos
