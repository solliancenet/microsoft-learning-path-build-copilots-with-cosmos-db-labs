---
title: '06 - Paginate cross-product query results with the Azure Cosmos DB for NoSQL SDK'
lab:
    title: '06 - Paginate cross-product query results with the Azure Cosmos DB for NoSQL SDK'
    module: 'Author complex queries with the Azure Cosmos DB for NoSQL'
layout: default
nav_order: 9
parent: 'JavaScript SDK labs'
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

## Import the @azure/cosmos library

The **@azure/cosmos** library is available on **npm** for easy installation into your JavaScript projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **javascript/06-sdk-pagination** folder.

1. Open the context menu for the **javascript/06-sdk-pagination** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **javascript/06-sdk-pagination** folder.

1. Initialize a new Node.js project:

    ```bash
    npm init -y
    ```

1. Install the [@azure/cosmos][npmjs.com/package/@azure/cosmos] package using the following command:

    ```bash
    npm install @azure/cosmos
    ```

## Iterate over the results of a SQL query using the SDK

When processing query results, you must make sure your code progresses through all pages of results and checks to see if any more pages are remaining before making subsequent requests.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **javascript/06-sdk-pagination** folder.

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

1. Create a new method named **paginateResults** and code to execute that method when you run the script. You will add the code to query the container within this method:

    ```javascript
    async function paginateResults() {
        // Query the container
    }

    paginateResults().catch((error) => {
        console.error(error);
    });
    ```

1. Inside the **paginateResults** method, add the following code to connect to the database and container you created earlier::

    ```javascript
    const database = client.database("cosmicworks");
    const container = database.container("products");
    ```

1. Create a query string variable named `sql` with a value of `SELECT * FROM products p`.

    ```javascript
    const sql = "SELECT * FROM products p";
    ```

1. Create a new variable named `options` and set it to an object with the `enableCrossPartitionQuery` property set to `true`. This property allows sending more than one request to execute the query in the Azure Cosmos DB service. More than one request is necessary if the query is not scoped to a single partition key value. Set the `maxItemCount` property to `50` to limit the number of items per page:

    ```javascript
    const options = {
        enableCrossPartitionQuery: true,
        maxItemCount: 50 // Set the maximum number of items per page
    };
    ```

1. Invoke the [`query`](https://learn.microsoft.com/javascript/api/%40azure/cosmos/items?view=azure-node-latest#@azure-cosmos-items-query-1) method with the `sql` and `options` variables as parameters to the constructor. This method returns an iterator that can be used to fetch the next page of results:

    ```javascript
    const iterator = container.items.query(query, options);
    ```

1. Iterate over the paginated results and print the `id`, `name`, and `price` of each item. The `iterator.getAsyncIterator` method returns an async iterator that can be used to fetch the `for await...of` loop to retrieve each page of results. This loop automatically handles the asynchronous iteration over the pages.

    ```javascript
    for await (const page of iterator.getAsyncIterator()) {
        page.resources.forEach(product => {
            console.log(`[${product.id}] ${product.name} $${product.price.toFixed(2)}`);
        });
    }
    ```

1. Your **script.js** file should now look like this:

    ```javascript
    const { CosmosClient } = require("@azure/cosmos");
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0

    const endpoint = "<cosmos-endpoint>";
    const key = "<cosmos-key>";

    const client = new CosmosClient({ endpoint, key });

    async function paginateResults() {
        const database = client.database("cosmicworks");
        const container = database.container("products");
        
        const query = "SELECT * FROM products WHERE products.price > 500";

        const options = {
            enableCrossPartitionQuery: true,
            maxItemCount: 50 // Set the maximum number of items per page
        };
        
        const iterator = container.items.query(query, options);

        for await (const page of iterator.getAsyncIterator()) {
            page.resources.forEach(product => {
                console.log(`[${product.id}] ${product.name} $${product.price.toFixed(2)}`);
            });
        }
    }
    
    paginateResults().catch((error) => {
        console.error(error);
    });
    ```

1. **Save** the **script.js** file.

1. Run the script to create the database and container:

    ```bash
    node script.js
    ```

1. The script will now output pages of 50 items at a time.

    > &#128161; The query will match hundreds of items in the products container.

1. Close the integrated terminal.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[npmjs.com/package/@azure/cosmos]: https://www.npmjs.com/package/@azure/cosmos
