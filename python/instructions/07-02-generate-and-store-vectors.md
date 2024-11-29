---
title: '07 - Generate vector embeddings with Azure OpenAI and store them in Azure Cosmos DB for NoSQL'
lab:
    title: '07 - Generate vector embeddings with Azure OpenAI and store them in Azure Cosmos DB for NoSQL'
    module: 'Build copilots with Python and Azure Cosmos DB for NoSQL'
layout: default
nav_order: 11
parent: 'Python SDK labs'
---

# Generate vector embeddings with Azure OpenAI and store them in Azure Cosmos DB for NoSQL

Azure OpenAI provides access to OpenAI's advanced language models, including the `text-embedding-ada-002`, `text-embedding-3-small`, and `text-embedding-3-large` models. By leveraging one of these models, you can generate vector representations of textual data, which can be stored in a vector store like Azure Cosmos DB for NoSQL. This facilitates efficient and accurate similarity searches, significantly enhancing a copilot's ability to retrieve relevant information and provide contextually rich interactions.

In this lab, you will create an Azure OpenAI service and deploy an embedding model. You will then use Python code to create Azure OpenAI and Cosmos DB clients using their respective Python SDKs to generate vector representations of product descriptions and write them into your database.

## Create an Azure OpenAI service

Azure OpenAI provides REST API access to OpenAI's powerful language models. These models can be easily adapted to your specific task including but not limited to content generation, summarization, image understanding, semantic search, and natural language to code translation.

1. In a new web browser window or tab, navigate to the Azure portal (``portal.azure.com``).

2. Sign into the portal using the Microsoft credentials associated with your subscription.

3. Select **Create a resource**, search for *Azure OpenAI*, and then create a new **Azure OpenAI** resource with the following settings, leaving all remaining settings to their default values:

    | Setting | Value |
    | ------- | ----- |
    | **Subscription** | *Your existing Azure subscription* |
    | **Resource group** | *Select an existing or create a new resource group* |
    | **Region** | *Choose an available region that supports the `text-embedding-3-small` model* from the [list of supporting regions](https://learn.microsoft.com/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-embeddings#tabpanel_3_standard-embeddings). |
    | **Name** | *Enter a globally unique name* |
    | **Pricing Tier** | *Choose Standard 0* |

    > &#128221; Your lab environments may have restrictions preventing you from creating a new resource group. If that is the case, use the existing pre-created resource group.

4. Wait for the deployment task to complete before continuing with the next task.

## Deploy an embedding model

To use Azure OpenAI to generate embeddings, you must first deploy an instance of the desired embedding model within your service.

1. Navigate to your newly created Azure OpenAI service in the Azure portal (``portal.azure.com``).

2. On the **Overview** page of the Azure OpenAI service, launch **Azure AI Studio** by selecting the **Go to Azure AI Studio** link on the toolbar.

3. In Azure AI Studio, select **Deployments** from the left-hand menu.

4. On the **Model deployments** page, select **Deploy model** and select **Deploy base model** from the dropdown.

5. From the list of models, select `text-embedding-3-small`.

    > &#128161; You can filter the list to display only *Embeddings* models using the inference tasks filter.

    > &#128221; If you do not see the `text-embedding-3-small` model, you may have selected an Azure region that does not currently support that model. In this case, you can use the `text-embedding-ada-002` model for this lab. Both models generate vectors with 1536 dimensions, so no changes are required to the container vector policy you defined on the `Products` container in Azure Cosmos DB.

6. Select **Confirm** to deploy the model.

7. On the **Model deployments** page in Azure AI Studio, note the **Name** of the `text-embedding-3-small` model deployment, as you will need this later in this exercise.

## Deploy a chat completion model

In addition to the embedding model, you will need a chat completion model for your copilot. You will use OpenAI's `gpt-4o` large language model to generate responses from your copilot.

1. While still on the **Model deployments** page in Azure AI Studio, select the **Deploy model** button again and choose **Deploy base model** from the dropdown.

2. Select the **gpt-4o** chat completion model from the list.

3. Select **Confirm** to deploy the model.

4. On the **Model deployments** page in Azure AI Studio, note the **Name** of the `gpt-4o` model deployment, as you will need this later in this exercise.

## Assign the Cognitive Services OpenAI User RBAC role

To allow your user identity to interact with the Azure OpenAI service, you can assign your account the **Cognitive Services OpenAI User** role. Azure OpenAI Service supports Azure role-based access control (Azure RBAC), an authorization system for managing individual access to Azure resources. Using Azure RBAC, you assign different team members different levels of permissions based on their needs for a given project.

1. In the Azure portal (``portal.azure.com``), navigate to your Azure OpenAI resource.

2. Select **Access Control (IAM)** on the left navigation pane.

3. Select **Add**, then select **Add role assignment**.

4. On the **Role** tab, select the **Cognitive Services OpenAI User** role, then select **Next**.

5. On the **Memebers** tab, select assign access to a user, group, or service principal, and select **Select members**.

6. In the **Select members** dialog, search for your name or email address and select your account.

7. On the **Review + assign** tab, select **Review + assign** to assign the role.

## Create a Python virtual environment

Virtual environments in Python are essential for maintaining a clean and organized development space, allowing individual projects to have their own set of dependencies, isolated from others. This prevents conflicts between different projects and ensures consistency in your development workflow. By using virtual environments, you can manage package versions easily, avoid dependency clashes, and keep your projects running smoothly. It's a best practice that keeps your coding environment stable and dependable, making your development process more efficient and less prone to issues.

1. In Visual Studio Code, open a new terminal window and change directories to the `python/07-build-copilot` folder.

2. Create a virtual environment named `.venv` by running the following command at the terminal prompt:

    ```bash
    python -m venv .venv 
    ```

    The able command will create a `.venv` folder under the `07-build-copilot` folder, which will provide a dedicated Python environment for the exercises in this lab.

3. Activate the virtual environment by selecting the appropriate command for your OS and shell from the table below and executing it at the terminal prompt.

    | Platform | Shell | Command to activate virtual environment |
    | -------- | ----- | --------------------------------------- |
    | POSIX | bash/zsh | `source .venv/bin/activate` |
    | | fish | `source .venv/bin/activate.fish` |
    | | csh/tcsh | `source .venv/bin/activate.csh` |
    | | pwsh | `.venv/bin/Activate.ps1` |
    | Windows | cmd.exe | `.venv\Scripts\activate.bat` |
    | | PowerShell | `.venv\Scripts\Activate.ps1` |

4. Install the libraries defined in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file contains a set of Python libraries you will use throughout this lab.

    | Library | Version | Description |
    | ------- | ------- | ----------- |
    | `azure-cosmos` | 4.9.0 | Azure Cosmos DB SDK for Python - Client library |
    | `azure-identity` | 1.19.0 | Azure Identity SDK for Python |
    | `fastapi` | 0.115.5 | Web framework for building APIs with Python |
    | `openai` | 1.55.2 | Provides access to the Azure OpenAI REST API from Python apps. |
    | `pydantic` | 2.10.2 | Data validation using Python type hints. |
    | `requests` | 2.32.3 | Send HTTP requests. |
    | `streamlit` | 1.40.2 | Transforms Python scripts into interactive web apps. |
    | `uvicorn` | 0.32.1 | An ASGI web server implementation for Python. |

## Create a Python function to vectorize text

The Python SDK for Azure OpenAI provides access to classes that can be used to create embeddings for textual data. This functionality can be encapsulated in a function in your Python code.

1. In the **Explorer** pane within Visual Studio Code, navigate to the `python/07-build-copilot/api/app` folder and open the `main.py` file located within it.

    > &#128221; This file will serve as the entry point to a backend Python API you will build in the next exercise. In this exercise, you will provide a handful of functions that can be used to import data with embeddings into Azure Cosmos DB that will be leveraged by the API.

2. To use the Azure OpenAI SDK for Python, import the library by adding the following code to the top of the `main.py` file:

    ```python
    from openai import AzureOpenAI
    ```

3. You will be accessing Azure OpenAI and Cosmos DB using Azure authentication and the RBAC roles you previously assigned to your Entra ID user identity. Add the following line below the `openai` import statement at the top of the file to import the required classes from the `azure-identity` library:

    ```python
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    ```

4. Create variables to store the Azure OpenAI API version and endpoint, replacing the `<AZURE_OPENAI_ENDPOINT>` token with the endpoint value for your Azure OpenAI service. Also, create a variable for the name of your embedding model deployment. Insert the following code below the `import` statements in the file:

    ```python
    # Azure OpenAI configuration
    AZURE_OPENAI_ENDPOINT = "<AZURE_OPENAI_ENDPOINT>"
    AZURE_OPENAI_API_VERSION = "2024-10-21"
    EMBEDDING_DEPLOYMENT_NAME = "text-embedding-3-small"
    ```

    > &#128161; The API version of `2024-10-21` was the latest GA release version as of the time of this writing. You can use that or a new version, if one is available. The API specs documentation contains a [table with the latest API versions](https://learn.microsoft.com/azure/ai-services/openai/reference#api-specs).

    > &#128221; The `EMBEDDING_DEPLOYMENT_NAME` is the **Name** value you noted after deploying the `text-embedding-3-small` model in Azure AI Studio. If you need to refer back to it, launch Azure AI Studio, navigate to the **Deployments** page and locate the deployment whose **Model name** is `text-embedding-3-small`. Then, copy the **Name** field value of that item. If you deployed the `text-embedding-ada-002` model, use the name for that deployment.

5. Use the Azure Identity SDK for Python's classes to create a token provider for accessing Azure OpenAI and a credential for connecting to Azure Cosmos DB by inserting the following code below the variable declarations:

    ```python
    # Enable Microsoft Entra ID RBAC authentication
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    ```

6. To handle the creation of embeddings, insert the following, which adds a function to generate embeddings using an Azure OpenAI client:

    ```python
    def generate_embeddings(text: str, model: str = "text-embedding-3-small"):
        client = AzureOpenAI(
            api_version = AZURE_OPENAI_API_VERSION,
            azure_endpoint = AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider = token_provider
        )

        response = client.embeddings.create(
            input = text,
            model = model
        )

        return response.data[0].embedding
    ```

7. The `main.py` file should now look similar to the following:

    ```python
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    # Azure OpenAI configuration
    AZURE_OPENAI_ENDPOINT = "<AZURE_OPENAI_ENDPOINT>"
    AZURE_OPENAI_API_VERSION = "2024-10-21"
    EMBEDDING_DEPLOYMENT_NAME = "text-embedding-3-small"

    # Enable Microsoft Entra ID RBAC authentication
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    def generate_embeddings(text: str, model: str = "text-embedding-3-small"):
        client = AzureOpenAI(
            api_version = AZURE_OPENAI_API_VERSION,
            azure_endpoint = AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider = token_provider
        )
    
        response = client.embeddings.create(
            input = text,
            model = model
        )
    
        return response.data[0].embedding
    ```

8. Save the `main.py` file.

## Test the embedding function

To test the `generate_embeddings` function in the `main.py` file, you will add a few lines of code at the bottom of the file. These lines allow you to execute the `generate_embeddings` function from the command line, passing in the text to embed.

1. At the bottom of the `main.py` file, add the following:

    ```python
    if __name__ == "__main__":
        import sys
        print(generate_embeddings(sys.argv[1]))
    ```

    > &#128221; This code is temporary and intended to provide a mechanism for quickly testing the `generate_embeddings` function. It will be overwritten later in this exercise.

2. Save the `main.py` file, which should now look like:

    ```python
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    
    # Azure OpenAI configuration
    AZURE_OPENAI_ENDPOINT = "<AZURE_OPENAI_ENDPOINT>"
    AZURE_OPENAI_API_VERSION = "2024-10-21"
    EMBEDDING_DEPLOYMENT_NAME = "text-embedding-3-small"
    
    # Use Microsoft Entra ID RBAC authentication
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    def generate_embeddings(text: str, model: str = "text-embedding-3-small"):
        client = AzureOpenAI(
            api_version = AZURE_OPENAI_API_VERSION,
            azure_endpoint = AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider = token_provider
        )
    
        response = client.embeddings.create(
            input = text,
            model = model
        )
    
        return response.data[0].embedding

    if __name__ == "__main__":
        import sys
        print(generate_embeddings(sys.argv[1]))
    ```

3. In Visual Studio Code, open a new integrated terminal window.

4. Ensure the intgrated terminal window is running within your Python virutal environment by activating your virtual environment using a command from the table below, selecting the appropriate command for your OS and shell.

    | Platform | Shell | Command to activate virtual environment |
    | -------- | ----- | --------------------------------------- |
    | POSIX | bash/zsh | `source .venv/bin/activate` |
    | | fish | `source .venv/bin/activate.fish` |
    | | csh/tcsh | `source .venv/bin/activate.csh` |
    | | pwsh | `.venv/bin/Activate.ps1` |
    | Windows | cmd.exe | `.venv\Scripts\activate.bat` |
    | | PowerShell | `.venv\Scripts\Activate.ps1` |

5. At the terminal prompt, change directories to `python/07-build-copilot/api/app`, then execute the following command:

    ```python
    python main.py "Hello, world!"
    ```

6. Observe the output in the terminal window. You should see an array of floating point number, which is the vector representation of the "Hello, world!" string. It should look similiar to the following abbreviated output:

    ```bash
    [-0.019184619188308716, -0.025279032066464424, -0.0017195191467180848, 0.01884828321635723...]
    ```

## Build a function for writing data to Azure Cosmos DB

Using the Azure Cosmos DB SDK for Python, you can create a function that allows upserting documents into your database. An upsert operation will update a record if a match is found and insert a new record if one is not.

1. In the `main.py` file in the `api/app` folder, import the `CosmosClient` class from the Azure Cosmos DB SDK for Python by inserting the following line just below the `import` statements already in the file:

    ```python
    from azure.cosmos import CosmosClient
    ```

2. Create a new group of variables containing configuration values associated with Azure Cosmos DB and add them to the `main.py` file below the Azure OpenAI variables you inserted previously. Ensure you replace the `<AZURE_COSMOSDB_ENDPOINT>` token with the endpoint for your Azure Cosmos DB account.

    ```python
    # Azure Cosmos DB configuration
    AZURE_COSMOSDB_ENDPOINT = "<AZURE_COSMOSDB_ENDPOINT>"
    DATABASE_NAME = "CosmicWorks"
    CONTAINER_NAME = "Products"
    ```

3. Add a function for upserting documents into Cosmos DB, inserting the following code below the `generate_embeddings` function in the `main.py` file:

    ```python
    def upsert_document(document: dict):
        # Create a Cosmos DB client
        cosmos_client = CosmosClient(url=AZURE_COSMOSDB_ENDPOINT, credential=credential)
        # Load the CosmicWorks database
        database = cosmos_client.get_database_client(DATABASE_NAME)
        # Retrieve the product container
        container = database.get_container_client(CONTAINER_NAME)
    
        # Upsert the document
        container.upsert_item(document)
    ```

4. Save the `main.py` file, which should now look like:

    ```python
    from openai import AzureOpenAI
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from azure.cosmos import CosmosClient
    
    # Azure OpenAI configuration
    AZURE_OPENAI_ENDPOINT = "<AZURE_OPENAI_ENDPOINT>"
    AZURE_OPENAI_API_VERSION = "2024-10-21"
    EMBEDDING_DEPLOYMENT_NAME = "text-embedding-3-small"
    
    # Azure Cosmos DB configuration
    AZURE_COSMOSDB_ENDPOINT = "<AZURE_COSMOSDB_ENDPOINT>"
    DATABASE_NAME = "CosmicWorks"
    CONTAINER_NAME = "Products"
    
    # Enable Microsoft Entra ID RBAC authentication
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    def generate_embeddings(text: str, model: str = "text-embedding-3-small"):
        client = AzureOpenAI(
            api_version = AZURE_OPENAI_API_VERSION,
            azure_endpoint = AZURE_OPENAI_ENDPOINT,
            azure_ad_token_provider = token_provider
        )
    
        response = client.embeddings.create(
            input = text,
            model = model
        )
    
        return response.data[0].embedding
    
    def upsert_document(document: dict):
        # Create a Cosmos DB client
        cosmos_client = CosmosClient(url=AZURE_COSMOSDB_ENDPOINT, credential=credential)
        # Load the CosmicWorks database
        database = cosmos_client.get_database_client(DATABASE_NAME)
        # Retrieve the product container
        container = database.get_container_client(CONTAINER_NAME)
    
        # Upsert the document
        container.upsert_item(document)
    
    if __name__ == "__main__":
        import sys
        print(generate_embeddings(sys.argv[1]))
    ```

## Vectorize sample data

To test both the `generate_embeddings` and `upsert_document` functions together, you will overwrite the `if __name__ == "__main__"` statement with code that downloads a sample data file containing Cosmic Works product information from GitHub and then vectorizes the `description` field of each product, and upserts the documents into the `Products` container in your Azure Cosmos DB database.

> &#128221; This approach is being used to demonstrate the techniques for generating with Azure OpenAI and storing embeddings in Azure Cosmos DB. In a real-world scenario, however, a more robust approach, such as using an Azure Function triggered by the Azure Cosmos DB change feed would be more appropiate for handling adding embeddings to existing and new documents.

1. In the `main.py` file in the `api/app` folder, overwrite the `if __name__ == "__main__":` code block with the following:

    ```python
    if __name__ == "__main__":
        from models import Product
        import requests
    
        product_raw_data = "https://raw.githubusercontent.com/solliancenet/microsoft-learning-path-build-copilots-with-cosmos-db-labs/refs/heads/main/data/07/products.json"
        products = [Product(**data) for data in requests.get(product_raw_data).json()]
    
        # Call the generate_embeddings function, passing in an argument from the command line.
        for product in products:
            product.embedding = generate_embeddings(product.description)
            upsert_document(product.model_dump())
    
        print("All products with vectorized descriptions have been upserted to the Cosmos DB container.")
    ```

    > &#128221; The line importing `Product` from the `models` module is taking advantage of a local Python class predefined within the project folder structure that reflects the shape of products from the Cosmic Works dataset.

2. At the open integrated terminal prompt, run the `main.py` file again using the command:

    ```python
    python main.py
    ```

3. Wait for the code execution to complete, indicated by a message indicating all products with vectorized descriptions have been upserted to the Cosmos DB container. It will take approximately ten minutes for the vectorization and data upsert process to complete.

## Review upserted sample data in Cosmos DB

1. Return to the Azure portal (``portal.azure.com``) and navigate to your Azure Cosmos DB account.

2. Select the Data Explorer for the left navigation menu.

3. Expand the **CosmicWorks** database and the **Products** container, and select **Items** under the container.

4. Select several random items within the container and ensure the `embedding` field is populated with the generated vector array.