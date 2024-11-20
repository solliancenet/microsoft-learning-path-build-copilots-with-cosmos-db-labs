
---
lab:
    title: 'Connect to Azure Cosmos DB for NoSQL with the SDK'
    module: 'Connect to Azure Cosmos DB for NoSQL with the SDK'
---

# Connect to Azure Cosmos DB for NoSQL with the SDK

The Azure SDK for Python is a suite of client libraries that provides a consistent developer interface to interact with many Azure services. Client libraries are packages that you would use to consume these resources and interact with them.

In this lab, you'll connect to an Azure Cosmos DB for NoSQL account using the Azure SDK for Python.

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

## Install the azure-cosmos library

The **azure-cosmos** library is available on **PyPI** for easy installation into your Python projects.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/01-sdk-connect** folder.

1. Open the context menu for the **python/01-sdk-connect** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

    > &#128221; This command will open the terminal with the starting directory already set to the **python/01-sdk-connect** folder.

1. Install the [azure-cosmos][pypi.org/project/azure-cosmos] package using the following command:

    ```bash
    pip install azure-cosmos
    ```

1. Close the integrated terminal.

## Use the azure-cosmos library

Once the Azure Cosmos DB library from the Azure SDK for Python has been imported, you can immediately use its classes to connect to an Azure Cosmos DB for NoSQL account. The **CosmosClient** class is the core class used to make the initial connection to an Azure Cosmos DB for NoSQL account.

1. In **Visual Studio Code**, in the **Explorer** pane, browse to the **python/01-sdk-connect** folder.

1. Open the blank Python file named **script.py**.

1. Add the following `import` statement to import the **CosmosClient** class:

    ```python
    from azure.cosmos import CosmosClient
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

1. Add a function named **main** to read and print account properties:

    ```python
    def main():
        account_info = client.client_connection.read_account()
        print(f"Account Name:	{account_info['id']}")
        print(f"Primary Region:	{account_info['writableLocations'][0]['name']}")

    if __name__ == "__main__":
        main()
    ```

1. Your **script.py** file should now look like this:

    ```python
    from azure.cosmos import CosmosClient

    endpoint = "<cosmos-endpoint>"
    key = "<cosmos-key>"

    client = CosmosClient(endpoint, key)

    def main():
        account_info = client.client_connection.read_account()
        print(f"Account Name:	{account_info['id']}")
        print(f"Primary Region:	{account_info['writableLocations'][0]['name']}")

    if __name__ == "__main__":
        main()
    ```

1. **Save** the **script.py** file.

## Test the script

Now that the Python code to connect to the Azure Cosmos DB for NoSQL account is complete, you can test the script. This script will print the name of the account and the name of the first writable region. When you created the account, you specified a location, and you should expect to see that same location value printed as the result of this script.

1. In **Visual Studio Code**, open the context menu for the **python/01-sdk-connect** folder and then select **Open in Integrated Terminal** to open a new terminal instance.

1. Run the script using the `python` command:

    ```bash
    python script.py
    ```

1. The script will now output the name of the account and the first writable region. For example, if you named the account **dp420**, and the first writable region was **West US 2**, the script would output:

    ```text
    Account Name:   dp420
    Primary Region: West US 2
    ```

1. Close the integrated terminal.

1. Close **Visual Studio Code**.

[code.visualstudio.com/docs/getstarted]: https://code.visualstudio.com/docs/getstarted/tips-and-tricks
[pypi.org/project/azure-cosmos]: https://pypi.org/project/azure-cosmos
