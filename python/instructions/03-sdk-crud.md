---
title: '03 - Create and update documents with the Azure Cosmos DB for NoSQL SDK'
lab:
    title: '03 - Create and update documents with the Azure Cosmos DB for NoSQL SDK'
    module: 'Implement Azure Cosmos DB for NoSQL point operations'
layout: default
nav_order: 6
parent: 'Python SDK labs'
---

# Create and update documents with the Azure Cosmos DB for NoSQL SDK

The `azure-cosmos` library includes methods to create, retrieve, update, and delete (CRUD) items within an Azure Cosmos DB for NoSQL container. Together, these methods perform some of the most common "CRUD" operations across various items within NoSQL API containers.

In this lab, you'll use the Python SDK to perform everyday CRUD operations on an item within an Azure Cosmos DB for NoSQL container.

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

1. Keep the browser tab open, as we will return to it later.

1. Switch back to **Visual Studio Code**.

## Install the azure-cosmos library

The **azure-cosmos** library is available on **PyPI** for easy installation into your Python projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/03-sdk-crud** folder.

1. Open the context menu for the **python/03-sdk-crud** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **python/03-sdk-crud** folder.

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

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/03-sdk-crud** folder.

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

## Perform create and read point operations on items with the SDK

You will now use the set of methods in the **ContainerProxy** class to perform common operations on items within a NoSQL API container.

1. Return to **Visual Studio Code**. If it is not still open, open the **script.py** code file within the **python/03-sdk-crud** folder.

1. Create a new product item and assign it to a variable named **saddle** with the following properties:

    | Property | Value |
    | ---: | :--- |
    | **id** | *706cd7c6-db8b-41f9-aea2-0e0c7e8eb009* |
    | **categoryId** | *9603ca6c-9e28-4a02-9194-51cdb7fea816* |
    | **name** | *Road Saddle* |
    | **price** | *45.99d* |
    | **tags** | *{ tan, new, crisp }* |

    ```python
    saddle = {
        "id": "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009",
        "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816",
        "name": "Road Saddle",
        "price": 45.99,
        "tags": ["tan", "new", "crisp"]
    }
    ```

1. Invoke the [`create_item`](https://learn.microsoft.com/python/api/azure-cosmos/azure.cosmos.container.containerproxy?view=azure-python#azure-cosmos-container-containerproxy-create-item) method of the **container** variable passing in the **saddle** variable as the method parameter:

    ```python
    container.create_item(body=saddle)
    ```

1. Once you are done, your code file should now include:
  
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

    saddle = {
        "id": "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009",
        "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816",
        "name": "Road Saddle",
        "price": 45.99,
        "tags": ["tan", "new", "crisp"]
    }
    
    container.create_item(body=saddle)
    ```

1. **Save** and run the script again:

    ```bash
    python script.py
    ```

1. Observe the new item in the **Data Explorer**.

1. Return to **Visual Studio Code**.

1. Return to the editor tab for the **script.py** code file.

1. Delete the following lines of code:

    ```python
    saddle = {
        "id": "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009",
        "categoryId": "9603ca6c-9e28-4a02-9194-51cdb7fea816",
        "name": "Road Saddle",
        "price": 45.99,
        "tags": ["tan", "new", "crisp"]
    }
    
    container.create_item(body=saddle)
    ```

1. Create a string variable named **item_id** with a value of **706cd7c6-db8b-41f9-aea2-0e0c7e8eb009**:

    ```python
    item_id = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009"
    ```

1. Create a string variable named **partition_key** with a value of **9603ca6c-9e28-4a02-9194-51cdb7fea816**:

    ```python
    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"
    ```

1. Invoke the [`read_item`](https://learn.microsoft.com/python/api/azure-cosmos/azure.cosmos.container.containerproxy?view=azure-python#azure-cosmos-container-containerproxy-read-item) method of the **container** variable passing in the **item_id** and **partition_key** variables as the method parameters:

    ```python
    # Read item    
    saddle = container.read_item(item=item_id, partition_key=partition_key)
    ```

1. Print the saddle object using a formatted output string:

    ```python
    print(f'[{saddle["id"]}]\t{saddle["name"]} ({saddle["price"]})')
    ```

1. Once you are done, your code file should now include:

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

    item_id = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009"
    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"
    
    # Read item
    saddle = container.read_item(item=item_id, partition_key=partition_key)
    
    print(f'[{saddle["id"]}]\t{saddle["name"]} ({saddle["price"]})')
    ```

1. **Save** and run the script again:

    ```bash
    python script.py
    ```

1. Observe the output from the terminal. Specifically, observe the formatted output text with the id, name, and price from the item.

## Perform update and delete point operations with the SDK

While learning the SDK, it's not uncommon to use an online Azure Cosmos DB account or the emulator to update an item and oscillate back-and-forth between the Data Explorer and your IDE of choice as you perform an operation and check to see if your change has been applied. Here, you will do just that as you update and delete an item using the SDK.

1. Return to your web browser window or tab.

1. Within the **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, expand the **cosmicworks** database node, then expand the new **products** container node within the **NOSQL API** navigation tree.

1. Select the **Items** node. Select the only item within the container and then observe the values of the **name** and **price** properties of the item.

    | **Property** | **Value** |
    | ---: | :--- |
    | **Name** | *Road Saddle* |
    | **Price** | *$45.99* |

    > &#128221; At this point in time, these values should not have been changed since you have created the item. You will change these values in this exercise.

1. Return to **Visual Studio Code**. Return to the editor tab for the **script.py** code file.

1. Delete the following line of code:

    ```python
    print(f'[{saddle["id"]}]\t{saddle["name"]} ({saddle["price"]})')
    ```

1. Change the **saddle** variable by setting the value of the price property to **32.55**:

    ```python
    saddle["price"] = 32.55
    ```

1. Modify the **saddle** variable again by setting the value of the **name** property to **Road LL Saddle**:

    ```python
    saddle["name"] = "Road LL Saddle"
    ```

1. Invoke the [`replace_item`](https://learn.microsoft.com/python/api/azure-cosmos/azure.cosmos.container.containerproxy?view=azure-python#azure-cosmos-container-containerproxy-replace-item) method of the **container** variable passing in the **item_id** and **saddle** variables as method parameters:

    ```python
    container.replace_item(item=item_id, body=saddle)
    ```

1. Once you are done, your code file should now include:

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
    
    item_id = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009"
    partition_key = "9603ca6c-9e28-4a02-9194-51cdb7fea816"
    
    # Read item
    saddle = container.read_item(item=item_id, partition_key=partition_key)
    
    saddle["price"] = 32.55
    saddle["name"] = "Road LL Saddle"
    
    container.replace_item(item=item_id, body=saddle)
    ```

1. **Save** and run the script again:

    ```bash
    python script.py
    ```

1. Return to your web browser window or tab.

1. Within the **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, expand the **cosmicworks** database node, then expand the new **products** container node within the **NOSQL API** navigation tree.

1. Select the **Items** node. Select the only item within the container and then observe the values of the **name** and **price** properties of the item.

    | **Property** | **Value** |
    | ---: | :--- |
    | **Name** | *Road LL Saddle* |
    | **Price** | *$32.55* |

    > &#128221; At this point in time, these values should  have been changed since you have observed the item.

1. Return to **Visual Studio Code**. Return to the editor tab for the **script.py** code file.

1. Delete the following lines of code:

    ```python
    # Read item
    saddle = container.read_item(item=item_id, partition_key=partition_key)
    
    saddle["price"] = 32.55
    saddle["name"] = "Road LL Saddle"
    
    container.replace_item(item=item_id, body=saddle)
    ```

1. Invoke the [`delete_item`](https://learn.microsoft.com/python/api/azure-cosmos/azure.cosmos.container.containerproxy?view=azure-python#azure-cosmos-container-containerproxy-delete-item) method of the **container** variable passing in the **item_id** and **partition_key** variables as method parameters:

    ```python
    # Delete the item
    container.delete_item(item=item_id, partition_key=partition_key)
    ```

1. Save and run the script again:

    ```bash
    python script.py
    ```

1. Close the integrated terminal.

1. Return to your web browser window or tab.

1. Within the **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, expand the **cosmicworks** database node, then expand the new **products** container node within the **NOSQL API** navigation tree.

1. Select the **Items** node. Observe that the items list is now empty.

1. Close your web browser window or tab.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[pypi.org/project/azure-cosmos]: https://pypi.org/project/azure-cosmos
