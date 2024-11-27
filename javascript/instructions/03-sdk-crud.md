---
title: '03 - Create and update documents with the Azure Cosmos DB for NoSQL SDK'
lab:
    title: '03 - Create and update documents with the Azure Cosmos DB for NoSQL SDK'
    module: 'Implement Azure Cosmos DB for NoSQL point operations'
layout: default
nav_order: 6
parent: 'JavaScript SDK labs'
---

# Create and update documents with the Azure Cosmos DB for NoSQL SDK

The `@azure/cosmos` library includes methods to create, retrieve, update, and delete (CRUD) items within an Azure Cosmos DB for NoSQL container. Together, these methods perform some of the most common "CRUD" operations across various items within NoSQL API containers.

In this lab, you'll use the JavaScript SDK to perform everyday CRUD operations on an item within an Azure Cosmos DB for NoSQL container.

## Prepare your development environment

If you have not already cloned the lab code repository for **Build copilots with Azure Cosmos DB** to the environment where you're working on this lab, follow these steps to do so. Otherwise, open the previously cloned folder in **Visual Studio Code**.

1. Start **Visual Studio Code**.

    > &#128221; If you are not already familiar with the Visual Studio Code interface, review the [Get Started guide for Visual Studio Code][code.visualstudio.com/docs/getstarted]

1. Open the command palette and run **Git: Clone** to clone the ``https://github.com/solliancenet/microsoft-learning-path-build-copilots-with-cosmos-db-labs`` GitHub repository in a local folder of your choice.

    > &#128161; You can use the **CTRL+SHIFT+P** keyboard shortcut to open the command palette.

1. Once the repository has been cloned, open the local folder you selected in **Visual Studio Code**.

## Create an Azure Cosmos DB for NoSQL account

Azure Cosmos DB is a cloud-based NoSQL database service that supports multiple APIs. When provisioning an Azure Cosmos DB account for the first time, you will select which of the APIs you want the account to support (for example, **Mongo API** or **NoSQL API**). Once the Azure Cosmos DB for NoSQL account is done provisioning, you can retrieve the endpoint and key and use them to connect to the Azure Cosmos DB for NoSQL account using the Azure SDK for JavaScript or any other SDK of your choice.

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

## Import the @azure/cosmos library

The **@azure/cosmos** library is available on **npm** for easy installation into your JavaScript projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **javascript/03-sdk-crud** folder.

1. Open the context menu for the **javascript/03-sdk-crud** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **javascript/03-sdk-crud** folder.

1. Initialize a new Node.js project:

    ```bash
    npm init -y
    ```

1. Install the [@azure/cosmos][npmjs.com/package/@azure/cosmos] package using the following command:

    ```bash
    npm install @azure/cosmos
    ```

## Use the @azure/cosmos library

Once the Azure Cosmos DB library from the Azure SDK for JavaScript has been imported, you can immediately use its classes to connect to an Azure Cosmos DB for NoSQL account. The **CosmosClient** class is the core class used to make the initial connection to an Azure Cosmos DB for NoSQL account.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **javascript/03-sdk-crud** folder.

1. Open the empty JavaScript file named **script.js**.

1. Add the following `require` statement to import the **@azure/cosmos** library:

    ```javascript
    const { CosmosClient } = require("@azure/cosmos");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0
    ```

1. Add variables named **endpoint** and **key** and set their values to the **endpoint** and **key** of the Azure Cosmos DB account you created earlier.

    ```javascript
    const endpoint = "<cosmos-endpoint>";
    const key = "<cosmos-key>";
    ```

    > &#128221; For example, if your endpoint is: **https://dp420.documents.azure.com:443/**, the statement would be: **const endpoint = "https://dp420.documents.azure.com:443/";**.

    > &#128221; If your key is: **fDR2ci9QgkdkvERTQ==**, the statement would be: **const key = "fDR2ci9QgkdkvERTQ==";**.

1. Add a new variable named **client** and initialize it as a new instance of the **CosmosClient** class using the **endpoint** and **key** variables:

    ```javascript
    const client = new CosmosClient({ endpoint, key });
    ```

1. Add the following code to create a database and container if they do not already exist:

    ```javascript
    async function main() {
        // Create database
        const { database } = await client.databases.createIfNotExists({ id: "cosmicworks" });
        
        // Create container
        const { container } = await database.containers.createIfNotExists({
            id: "products",
            partitionKey: { paths: ["/categoryId"] },
            throughput: 400
        });
    }
    
    main().catch((error) => console.error(error));
    ```

1. Your **script.js** file should now look like this:

    ```javascript
    const { CosmosClient } = require("@azure/cosmos");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0

    const endpoint = "<cosmos-endpoint>";
    const key = "<cosmos-key>";

    const client = new CosmosClient({ endpoint, key });

    async function main() {
        // Create database
        const { database } = await client.databases.createIfNotExists({ id: "cosmicworks" });
        
        // Create container
        const { container } = await database.containers.createIfNotExists({
            id: "products",
            partitionKey: { paths: ["/categoryId"] },
            throughput: 400
        });
    }
    
    main().catch((error) => console.error(error));
    ```

1. **Save** the **script.js** file.

1. Run the script to create the database and container:

    ```bash
    node script.js
    ```

1. Switch to your web browser window.

1. Within the **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, expand the **cosmicworks** database node, then observe the new **products** container node within the **NOSQL API** navigation tree.

## Perform create and read point operations on items with the SDK

You will now use the set of methods in the **Container** class to perform common operations on items within a NoSQL API container.

1. Return to **Visual Studio Code**. If it is not still open, open the **script.js** code file within the **javascript/03-sdk-crud** folder.

1. Create a new product item and assign it to a variable named **saddle** with the following properties. Make sure you add the following code into the `main` function:

    | Property | Value |
    | ---: | :--- |
    | **id** | *706cd7c6-db8b-41f9-aea2-0e0c7e8eb009* |
    | **categoryId** | *9603ca6c-9e28-4a02-9194-51cdb7fea816* |
    | **name** | *Road Saddle* |
    | **price** | *45.99d* |
    | **tags** | *{ tan, new, crisp }* |

    ```javascript
    const saddle = {
        id: "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009",
        categoryId: "9603ca6c-9e28-4a02-9194-51cdb7fea816",
        name: "Road Saddle",
        price: 45.99,
        tags: ["tan", "new", "crisp"]
    };
    ```

1. Invoke the [`create`](https://learn.microsoft.com/javascript/api/%40azure/cosmos/items?view=azure-node-latest#@azure-cosmos-items-create) method of the container's **items** class, passing in the **saddle** variable as the method parameter:

    ```javascript
    const { resource: item } = await container
        .items.create(saddle);
    ```

1. Once you are done, your code file should now include:
  
    ```javascript
    const { CosmosClient } = require("@azure/cosmos");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0

    const endpoint = "<cosmos-endpoint>";
    const key = "<cosmos-key>";

    const client = new CosmosClient({ endpoint, key });

    async function main() {
        // Create database
        const { database } = await client.databases.createIfNotExists({ id: "cosmicworks" });
            
        // Create container
        const { container } = await database.containers.createIfNotExists({
            id: "products",
            partitionKey: { paths: ["/categoryId"] },
            throughput: 400
        });
    
        const saddle = {
            id: "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009",
            categoryId: "9603ca6c-9e28-4a02-9194-51cdb7fea816",
            name: "Road Saddle",
            price: 45.99,
            tags: ["tan", "new", "crisp"]
        };
    
        const { resource: item } = await container
                .items.create(saddle);
    }
    
    main().catch((error) => console.error(error));
    ```

1. **Save** and run the script again:

    ```bash
    node script.js
    ```

1. Observe the new item in the **Data Explorer**.

1. Return to **Visual Studio Code**.

1. Return to the editor tab for the **script.js** code file.

1. Delete the following lines of code:

    ```javascript
    const saddle = {
        id: "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009",
        categoryId: "9603ca6c-9e28-4a02-9194-51cdb7fea816",
        name: "Road Saddle",
        price: 45.99,
        tags: ["tan", "new", "crisp"]
    };

    const { resource: item } = await container
            .items.create(saddle);
    ```

1. Create a string variable named **item_id** with a value of **706cd7c6-db8b-41f9-aea2-0e0c7e8eb009**:

    ```javascript
    const itemId = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009";
    ```

1. Create a string variable named **partition_key** with a value of **9603ca6c-9e28-4a02-9194-51cdb7fea816**:

    ```javascript
    const partitionKey = "9603ca6c-9e28-4a02-9194-51cdb7fea816";
    ```

1. Invoke the [`read`](https://learn.microsoft.com/javascript/api/%40azure/cosmos/item?view=azure-node-latest#@azure-cosmos-item-read) method of the container's **item** class, passing in the **itemId** and **partitionKey** variables as the method parameters:

    ```javascript
    // Read the item
    const { resource: saddle } = await container.item(itemId, partitionKey).read();
    ```

1. Print the saddle object using a formatted output string:

    ```javascript
    print(f'[{saddle["id"]}]\t{saddle["name"]} ({saddle["price"]})')
    ```

1. Once you are done, your code file should now include:

    ```javascript
    const { CosmosClient } = require("@azure/cosmos");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0
    
    const endpoint = "<cosmos-endpoint>";
    const key = "<cosmos-key>";
    
    const client = new CosmosClient({ endpoint, key });

    async function main() {
        // Create database
        const { database } = await client.databases.createIfNotExists({ id: "cosmicworks" });
            
        // Create container
        const { container } = await database.containers.createIfNotExists({
            id: "products",
            partitionKey: { paths: ["/categoryId"] },
            throughput: 400
        });
    
        const itemId = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009";
        const partitionKey = "9603ca6c-9e28-4a02-9194-51cdb7fea816";
    
        // Read the item
        const { resource: saddle } = await container.item(itemId, partitionKey).read();
    
        console.log(`[${saddle.id}]\t${saddle.name} (${saddle.price})`);
    }
    
    main().catch((error) => console.error(error));
    ```

1. **Save** and run the script again:

    ```bash
    node script.js
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

1. Return to **Visual Studio Code**. Return to the editor tab for the **script.js** code file.

1. Delete the following line of code:

    ```javascript
    console.log(`[${saddle.id}]\t${saddle.name} (${saddle.price})`);
    ```

1. Change the **saddle** variable by setting the value of the price property to **32.55**:

    ```javascript
    // Update the item
    saddle.price = 32.55;
    ```

1. Modify the **saddle** variable again by setting the value of the **name** property to **Road LL Saddle**:

    ```javascript
    saddle.name = "Road LL Saddle";
    ```

1. Invoke the [`replace`](https://learn.microsoft.com/javascript/api/%40azure/cosmos/item?view=azure-node-latest#@azure-cosmos-item-replace) method of the container's **item** class, passing in the **saddle** variable as a method parameter:

    ```javascript
    await container.item(saddle.id, partitionKey).replace(saddle);
    ```

1. Once you are done, your code file should now include:

    ```javascript
    const { CosmosClient } = require("@azure/cosmos");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0
    
    const endpoint = "<cosmos-endpoint>";
    const key = "<cosmos-key>";
    
    const client = new CosmosClient({ endpoint, key });

    async function main() {
        // Create database
        const { database } = await client.databases.createIfNotExists({ id: "cosmicworks" });
            
        // Create container
        const { container } = await database.containers.createIfNotExists({
            id: "products",
            partitionKey: { paths: ["/categoryId"] },
            throughput: 400
        });
    
        const itemId = "706cd7c6-db8b-41f9-aea2-0e0c7e8eb009";
        const partitionKey = "9603ca6c-9e28-4a02-9194-51cdb7fea816";
    
        // Read the item
        const { resource: saddle } = await container.item(itemId, partitionKey).read();

        // Update the item
        saddle.price = 32.55;
        saddle.name = "Road LL Saddle";
    
        await container.item(saddle.id, partitionKey).replace(saddle);
    }
    
    main().catch((error) => console.error(error));
    ```

1. **Save** and run the script again:

    ```bash
    node script.js
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

1. Return to **Visual Studio Code**. Return to the editor tab for the **script.js** code file.

1. Delete the following lines of code:

    ```javascript
    // Read the item
    const { resource: saddle } = await container.item(itemId, partitionKey).read();

    // Update the item
    saddle.price = 32.55;
    saddle.name = "Road LL Saddle";

    await container.item(saddle.id, partitionKey).replace(saddle);
    ```

1. Invoke the [`delete`](https://learn.microsoft.com/javascript/api/%40azure/cosmos/item?view=azure-node-latest#@azure-cosmos-item-delete) method of the container's **item** class, passing in the **itemId** and **partitionKey** variables as method parameters:

    ```javascript
    // Delete the item
    await container.item(itemId, partitionKey).delete();
    ```

1. Save and run the script again:

    ```bash
    node script.js
    ```

1. Close the integrated terminal.

1. Return to your web browser window or tab.

1. Within the **Azure Cosmos DB** account resource, navigate to the **Data Explorer** pane.

1. In the **Data Explorer**, expand the **cosmicworks** database node, then expand the new **products** container node within the **NOSQL API** navigation tree.

1. Select the **Items** node. Observe that the items list is now empty.

1. Close your web browser window or tab.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[npmjs.com/package/@azure/cosmos]: https://www.npmjs.com/package/@azure/cosmos
