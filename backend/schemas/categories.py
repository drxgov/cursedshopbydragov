from pydantic import BaseModel


class CategoryCreate(BaseModel):
    title: str
    description: str | None = None


class CategoryRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    model_config = {"from_attributes": True}


class CategoryUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
