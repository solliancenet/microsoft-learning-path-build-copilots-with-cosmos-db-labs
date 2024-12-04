---
title: '04 - Batch multiple point operations together with the Azure Cosmos DB for NoSQL SDK'
lab:
    title: '04 - Batch multiple point operations together with the Azure Cosmos DB for NoSQL SDK'
    module: 'Perform cross-document transactional operations with the Azure Cosmos DB for NoSQL'
layout: default
nav_order: 7
parent: 'Python SDK labs'
---

# Batch multiple point operations together with the Azure Cosmos DB for NoSQL SDK

The `azure-cosmos` Python SDK provides the `execute_item_batch` method for executing multiple point operations in a single logical step. This allows developers to efficiently bundle multiple operations together and determine if they completed successfully server-side.

In this lab, you'll use the Python SDK to perform dual-item batch operations that demonstrate both successful and errant transactional batches.

## Prepare your development environment

If you have not already cloned the lab code repository for **Build copilots with Azure Cosmos DB** to the environment where you're working on this lab, follow these steps to do so. Otherwise, open the previously cloned folder in **Visual Studio Code**.

1. Start **Visual Studio Code**.

    > &#128221; If you are not already familiar with the Visual Studio Code interface, review the [Get Started guide for Visual Studio Code][code.visualstudio.com/docs/getstarted]

1. Open the command palette and run **Git: Clone** to clone the ``https://github.com/solliancenet/microsoft-learning-path-build-copilots-with-cosmos-db-labs`` GitHub repository in a local folder of your choice.

    > &#128161; You can use the **CTRL+SHIFT+P** keyboard shortcut to open the command palette.

1. Once the repository has been cloned, open the local folder you selected in **Visual Studio Code**.

## Create an Azure Cosmos DB for NoSQL account

If you already created an Azure Cosmos DB for NoSQL account for the **Build copilots with Azure Cosmos DB** labs on this site, you can use it for this lab and skip ahead to the [next section](#install-the-azure-cosmos-library). Otherwise, follow the steps below to create a new Azure Cosmos DB for NoSQL account.

<details markdown=1>
<summary markdown="span"><strong>Click to expand/collapse steps to create an Azure Cosmos DB for NoSQL account</strong></summary>

Azure Cosmos DB is a cloud-based NoSQL database service that supports multiple APIs. When provisioning an Azure Cosmos DB account for the first time, you will select which of the APIs you want the account to support. Once the Azure Cosmos DB for NoSQL account is done provisioning, you can retrieve the endpoint and key and use them to connect to the Azure Cosmos DB for NoSQL account using the Azure SDK for Python or any other SDK of your choice.

1. In a new web browser window or tab, navigate to the Azure portal (``portal.azure.com``).

2. Sign into the portal using the Microsoft credentials associated with your subscription.

3. Select **+ Create a resource**, search for *Cosmos DB*, and then create a new **Azure Cosmos DB for NoSQL** account resource with the following settings, leaving all remaining settings to their default values:

    | **Setting** | **Value** |
    | ---: | :--- |
    | **Subscription** | *Your existing Azure subscription* |
    | **Resource group** | *Select an existing or create a new resource group* |
    | **Account Name** | *Enter a globally unique name* |
    | **Location** | *Choose any available region* |
    | **Capacity mode** | *Serverless* |
    | **Apply Free Tier Discount** | *Do Not Apply* |

    > &#128221; Your lab environments may have restrictions preventing you from creating a new resource group. If that is the case, use the existing pre-created resource group.

4. Wait for the deployment task to complete before continuing with this task.

5. Go to the newly created **Azure Cosmos DB** account resource and navigate to the **Keys** pane.

6. This pane contains the connection details and credentials necessary to connect to the account from the SDK. Specifically:

    1. Notice the **URI** field. You will use this **endpoint** value later in this exercise.

    2. Notice the **PRIMARY KEY** field. You will use this **key** value later in this exercise.

7. Keep the browser tab open, as we will return to it later.

</details>

## Install the azure-cosmos library

The **azure-cosmos** library is available on **PyPI** for easy installation into your Python projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/04-sdk-batch** folder.

1. Open the context menu for the **python/04-sdk-batch** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **python/04-sdk-batch** folder.

1. Create and activate a virtual environment to manage dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

1. Install the [azure-cosmos][pypi.org/project/azure-cosmos] package using the following command:

    ```bash
    pip install azure-cosmos
    ```

## Use the azure-cosmos library

Using the credentials from the newly created account, you will connect with the SDK classes and create a new database and container instance. Then, you will use the Data Explorer to validate that the instances exist in the Azure portal.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/04-sdk-batch** folder.

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

1. Add the following code to create a database and container if they do not already exist:

    ```python
    # Create database
    database = client.create_database_if_not_exists(id="cosmicworks")
    
    # Create container
    container = database.create_container_if_not_exists(
        id="products",
        partition_key=PartitionKey(path="/categoryId"),
        offer_throughput=400
    )
    ```

1. Your **script.py** file should now look like this:

    ```python
    from azure.cosmos import CosmosClient, PartitionKey

    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"

    client = CosmosClient(endpoint, key)

    # Create database
    database = client.create_database_if_not_exists(id="cosmicworks")
    
    # Create container
    container = database.create_container_if_not_exists(
        id="products",
        partition_key=PartitionKey(path="/categoryId"),
        offer_throughput=400
    )
    ```

1. **Save** the **script.py** file.

1. Run the script to create the database and container:

    ```bash
    python script.py
    ```

1. Switch to your web browser window.

1. Within the **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, expand the **cosmicworks** database node, then observe the new **products** container node within the **NOSQL API** navigation tree.

## Creating a transactional batch

First, let's create a simple transactional batch that makes two fictional products. This batch will insert a worn saddle and a rusty handlebar into the container with the same "used accessories" category identifier. Both items have the same logical partition key, ensuring that we will have a successful batch operation.

1. Return to **Visual Studio Code**. If it is not still open, open the **script.py** code file within the **python/04-sdk-batch** folder.

1. Create two dictionaries representing products: a **worn saddle** and a **rusty handlebar**. Both items share the same partition key value of **"9603ca6c-9e28-4a02-9194-51cdb7fea816"**.

    ```python
    saddle = ("create", (
        {"id": "0120", "name": "Worn Saddle", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))

    handlebar = ("create", (
        {"id": "012A", "name": "Rusty Handlebar", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))
    ```

1. Define the partition key value.

    ```python
    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"
    ```

1. Create a batch containing the two items.

    ```python
    batch = [saddle, handlebar]
    ```

1. Execute the batch using the `execute_item_batch` method of the `container` object and print the response for each item in the batch.

```python
try:
        # Execute the batch
        batch_response = container.execute_item_batch(batch, partition_key=partition_key)

        # Print results for each operation in the batch
        for idx, result in enumerate(batch_response):
            status_code = result.get("statusCode")
            resource = result.get("resourceBody")
            print(f"Item {idx} - Status Code: {status_code}, Resource: {resource}")
    except exceptions.CosmosBatchOperationError as e:
        error_operation_index = e.error_index
        error_operation_response = e.operation_responses[error_operation_index]
        error_operation = batch[error_operation_index]
        print("Error operation: {}, error operation response: {}".format(error_operation, error_operation_response))
    except Exception as ex:
        print(f"An error occurred: {ex}")
```

1. Once you are done, your code file should now include:
  
    ```python
    from azure.cosmos import CosmosClient, PartitionKey, exceptions

    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"

    client = CosmosClient(endpoint, key)

    # Create database
    database = client.create_database_if_not_exists(id="cosmicworks")
    
    # Create container
    container = database.create_container_if_not_exists(
        id="products",
        partition_key=PartitionKey(path="/categoryId"),
        offer_throughput=400
    )

    saddle = ("create", (
        {"id": "0120", "name": "Worn Saddle", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))
    handlebar = ("create", (
        {"id": "012A", "name": "Rusty Handlebar", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))

    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"

    batch = [saddle, handlebar]
    
    try:
        # Execute the batch
        batch_response = container.execute_item_batch(batch, partition_key=partition_key)

        # Print results for each operation in the batch
        for idx, result in enumerate(batch_response):
            status_code = result.get("statusCode")
            resource = result.get("resourceBody")
            print(f"Item {idx} - Status Code: {status_code}, Resource: {resource}")
    except exceptions.CosmosBatchOperationError as e:
        error_operation_index = e.error_index
        error_operation_response = e.operation_responses[error_operation_index]
        error_operation = batch[error_operation_index]
        print("Error operation: {}, error operation response: {}".format(error_operation, error_operation_response))
    except Exception as ex:
        print(f"An error occurred: {ex}")
    ```

1. **Save** and run the script again:

    ```bash
    python script.py
    ```

1. The output should indicate a successful status code for each operation.

## Creating an errant transactional batch

Now, let’s create a transactional batch that will error purposefully. This batch will attempt to insert two items that have different logical partition keys. We will create a flickering strobe light in the "used accessories" category and a new helmet in the "pristine accessories" category. By definition, this should be a bad request and return an error when performing this transaction.

1. Return to the editor tab for the **script.py** code file.

1. Delete the following lines of code:

    ```python
    saddle = ("create", (
        {"id": "0120", "name": "Worn Saddle", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))
    handlebar = ("create", (
        {"id": "012A", "name": "Rusty Handlebar", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))

    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"

    batch = [saddle, handlebar]
    ```

1. Modify the script to create a new **flickering strobe light** and a **new helmet** with different partition key values.

    ```python
    light = ("create", (
        {"id": "012B", "name": "Flickering Strobe Light", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))
    helmet = ("create", (
        {"id": "012C", "name": "New Helmet", "categoryId": "0feee2e4-687a-4d69-b64e-be36afc33e74"},
    ))
    ```

1. Define the partition key value for the batch.

    ```python
    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"
    ```

1. Create a new batch containing the two items.

    ```python
    batch = [light, helmet]
    ```

1. Once you are done, your code file should now include:

    ```python
    from azure.cosmos import CosmosClient, PartitionKey, exceptions

    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"

    client = CosmosClient(endpoint, key)

    # Create database
    database = client.create_database_if_not_exists(id="cosmicworks")
    
    # Create container
    container = database.create_container_if_not_exists(
        id="products",
        partition_key=PartitionKey(path="/categoryId"),
        offer_throughput=400
    )

    light = ("create", (
        {"id": "012B", "name": "Flickering Strobe Light", "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816"},
    ))
    helmet = ("create", (
        {"id": "012C", "name": "New Helmet", "categoryId": "0feee2e4-687a-4d69-b64e-be36afc33e74"},
    ))

    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"

    batch = [light, helmet]
    
    try:
        # Execute the batch
        batch_response = container.execute_item_batch(batch, partition_key=partition_key)

        # Print results for each operation in the batch
        for idx, result in enumerate(batch_response):
            status_code = result.get("statusCode")
            resource = result.get("resourceBody")
            print(f"Item {idx} - Status Code: {status_code}, Resource: {resource}")
    except exceptions.CosmosBatchOperationError as e:
        error_operation_index = e.error_index
        error_operation_response = e.operation_responses[error_operation_index]
        error_operation = batch[error_operation_index]
        print("Error operation: {}, error operation response: {}".format(error_operation, error_operation_response))
    except Exception as ex:
        print(f"An error occurred: {ex}")
    ```

1. **Save** and run the script again:

    ```bash
    python script.py
    ```

1. Observe the output from the terminal. The status code on the second item (the "New Helmet") should be **400** for **Bad Request**. This occurred because all items within the transaction did not share the same partition key value as the transactional batch.

1. Close the integrated terminal.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[pypi.org/project/azure-cosmos]: https://pypi.org/project/azure-cosmos
