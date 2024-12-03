import uuid
from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str = Field(str(uuid.uuid4()), description="Unique identifier for the product")
    category_id: str = Field(..., description="Unique identifier for the product's category")
    category_name: str = Field(..., description="A comma-separated string containing the names associated with the product's category")
    sku: str = Field(..., alias="sku", description="Stock Keeping Unit (SKU) for the product")
    name: str = Field(..., alias="name", description="Name of the product")
    description: str = Field(..., alias="description", description="Description of the product")
    price: float = Field(..., alias="price", description="Price of the product")
    discount: float = Field(None, alias="discount", description="Discounted price of the product")
    sale_price: float = Field(None, alias="salePrice", description="Sale price of the product")
    embedding: list = Field([], alias="embedding", description="Vector representation of the product description")
