from pydantic import BaseModel, Field

class Product(BaseModel):
    id: str = Field(default=None, alias="id")
    category_id: str = Field(alias="categoryId")
    category_name: str = Field(alias="categoryName")
    sku: str
    name: str
    description: str
    price: float
    embedding: list = []
