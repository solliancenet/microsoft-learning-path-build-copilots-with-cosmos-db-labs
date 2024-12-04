---
title: '06 - Paginate cross-product query results with the Azure Cosmos DB for NoSQL SDK'
lab:
    title: '06 - Paginate cross-product query results with the Azure Cosmos DB for NoSQL SDK'
    module: 'Author complex queries with the Azure Cosmos DB for NoSQL'
layout: default
nav_order: 9
parent: 'Python SDK labs'
---

# Paginate cross-product query results with the Azure Cosmos DB for NoSQL SDK

Azure Cosmos DB queries will typically have multiple pages of results. Pagination is done automatically server-side when Azure Cosmos DB cannot return all query results in one single execution. In many applications, you will want to write code using the SDK to process your query results in batches in a performant manner.

In this lab, you'll create a feed iterator that can be used in a loop to iterate over your entire result set.

## Prepare your development environment

If you have not already cloned the lab code repository for **Build copilots with Azure Cosmos DB** to the environment where you're working on this lab, follow these steps to do so. Otherwise, open the previously cloned folder in **Visual Studio Code**.

1. Start **Visual Studio Code**.

    > &#128221; If you are not already familiar with the Visual Studio Code interface, review the [Get Started guide for Visual Studio Code][code.visualstudio.com/docs/getstarted]

1. Open the command palette and run **Git: Clone** to clone the ``https://github.com/solliancenet/microsoft-learning-path-build-copilots-with-cosmos-db-labs`` GitHub repository in a local folder of your choice.

    > &#128161; You can use the **CTRL+SHIFT+P** keyboard shortcut to open the command palette.

1. Once the repository has been cloned, open the local folder you selected in **Visual Studio Code**.

## Create an Azure Cosmos DB for NoSQL account

If you already created an Azure Cosmos DB for NoSQL account for the **Build copilots with Azure Cosmos DB** labs on this site, you can use it for this lab and skip ahead to the [next section](#create-azure-cosmos-db-database-and-container-with-sample-data). Otherwise, follow the steps below to create a new Azure Cosmos DB for NoSQL account.

<details markdown=1>
<summary markdown="span"><strong>Click to expand/collapse steps to create an Azure Cosmos DB for NoSQL account</strong></summary>

Azure Cosmos DB is a cloud-based NoSQL database service that supports multiple APIs. When provisioning an Azure Cosmos DB account for the first time, you will select which of the APIs you want the account to support. Once the Azure Cosmos DB for NoSQL account is done provisioning, you can retrieve the endpoint and key and use them to connect to the Azure Cosmos DB for NoSQL account using the Azure SDK for Python or any other SDK of your choice.

1. In a new web browser window or tab, navigate to the Azure portal (``portal.azure.com``).

1. Sign into the portal using the Microsoft credentials associated with your subscription.

1. Select **+ Create a resource**, search for *Cosmos DB*, and then create a new **Azure Cosmos DB for NoSQL** account resource with the following settings, leaving all remaining settings to their default values:

    | **Setting** | **Value** |
    | ---: | :--- |
    | **Subscription** | *Your existing Azure subscription* |
    | **Resource group** | *Select an existing or create a new resource group* |
    | **Account Name** | *Enter a globally unique name* |
    | **Location** | *Choose any available region* |
    | **Capacity mode** | *Serverless* |
    | **Apply Free Tier Discount** | *Do Not Apply* |

    > &#128221; Your lab environments may have restrictions preventing you from creating a new resource group. If that is the case, use the existing pre-created resource group.

1. Wait for the deployment task to complete before continuing with this task.

1. Go to the newly created **Azure Cosmos DB** account resource and navigate to the **Keys** pane.

1. This pane contains the connection details and credentials necessary to connect to the account from the SDK. Specifically:

    1. Notice the **URI** field. You will use this **endpoint** value later in this exercise.

    1. Notice the **PRIMARY KEY** field. You will use this **key** value later in this exercise.

</details>

## Create Azure Cosmos DB database and container with sample data

If you already created an Azure Cosmos DB database named **cosmicworks-full** and container within it named **products**, which is preloaded with sample data, you can use it for this lab and skip ahead to the [next section](#install-the-azure-cosmos-library). Otherwise, follow the steps below to create a new sample database and container.

<details markdown=1>
<summary markdown="span"><strong>Click to expand/collapse steps to create database and container with sample data</strong></summary>

1. Within the newly created **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, select **Launch quick start** on the home page.

1. Within the **New Container** form, enter the following values:

    - **Database id**: `cosmicworks-full`
    - **Container id**: `products`
    - **Partition key**: `/categoryId`
    - **Analytical store**: `Off`

1. Select **OK** to create the new container. This process will take a minute or two while it creates the resources and preloads the container with sample product data.

1. Keep the browser tab open, as we will return to it later.

1. Switch back to **Visual Studio Code**.

</details>

## Install the azure-cosmos library

The **azure-cosmos** library is available on **PyPI** for easy installation into your Python projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/06-sdk-pagination** folder.

1. Open the context menu for the **python/06-sdk-pagination** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **python/06-sdk-pagination** folder.

1. Create and activate a virtual environment to manage dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

1. Install the [azure-cosmos][pypi.org/project/azure-cosmos] package using the following command:

    ```bash
    pip install azure-cosmos
    ```

## Paginate through small result sets of a SQL query using the SDK

When processing query results, you must make sure your code progresses through all pages of results and checks to see if any more pages are remaining before making subsequent requests.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/06-sdk-pagination** folder.

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
    database = client.get_database_client("cosmicworks-full")
    container = database.get_container_client("products")
    ```

1. Create a new variable named **sql** of type *string* with a value of **SELECT p.id, p.name, p.price FROM products p**:

    ```python
    sql = "SELECT p.id, p.name, p.price FROM products p"
    ```

1. Invoke the [`query_items`](https://learn.microsoft.com/python/api/azure-cosmos/azure.cosmos.container.containerproxy?view=azure-python#azure-cosmos-container-containerproxy-query-items) method with the `sql` variable as a parameter to the constructor. The `enable_cross_partition_query`, when set to `True`, allows sending of more than one request to execute the query in the Azure Cosmos DB service. More than one request is necessary if the query is not scoped to single partition key value. Set the `max_item_count` to `50` to limit the number of items returned in each page.

    ```python
    iterator = container.query_items(
        query=sql,
        enable_cross_partition_query=True,
        max_item_count=50  # Set maximum items per page
    )
    ```

1. Create a **for** loop that invokes the [`by_page`](https://learn.microsoft.com/python/api/azure-core/azure.core.paging.itempaged?view=azure-python#azure-core-paging-itempaged-by-page) method on the iterator object. This method returns a page of results each time it is called.

    ```python
    for page in iterator.by_page():
    ```

1. Within the **for** loop, iterate over the paginated results and print the `id`, `name`, and `price` of each item.

    ```python
    for product in page:
        print(f"[{product['id']}]	{product['name']}	${product['price']:.2f}")
    ```

1. Your **script.py** file should now look like this:

    ```python
    from azure.cosmos import CosmosClient, PartitionKey

    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"

    client = CosmosClient(endpoint, key)

    database = client.get_database_client("cosmicworks-full")
    container = database.get_container_client("products")
    
    sql = "SELECT * FROM products WHERE products.price > 500"

    iterator = container.query_items(
        query=sql,
        enable_cross_partition_query=True,
        max_item_count=50  # Set maximum items per page
    )

    for page in iterator.by_page():
        for product in page:
            print(f"[{product['id']}]	{product['name']}	${product['price']:.2f}")
    ```

1. **Save** the **script.py** file.

1. Run the script to create the database and container:

    ```bash
    python script.py
    ```

1. The script will now output pages of 50 items at a time.

    > &#128161; The query will match hundreds of items in the products container.

1. Close the integrated terminal.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[pypi.org/project/azure-cosmos]: https://pypi.org/project/azure-cosmos
