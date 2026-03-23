from pydantic import BaseModel


class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = {
        "from_attributes": True,
    }
