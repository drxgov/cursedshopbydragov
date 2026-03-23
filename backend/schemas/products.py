from pydantic import BaseModel


class ProductCreate(BaseModel):
    title: str
    description: str
    price: int
    image_source: str | None = None
    count: int
    is_available: bool = True
    category_id: int


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    image_source: str | None = None
    count: int | None = None
    is_available: bool | None = None
    category_id: int | None = None
