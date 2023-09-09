from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    image: str
    rating: float = 0.0
    featuredRating: bool = False
    slug: str


class ProductCreate(ProductBase):
    type_id: int


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
