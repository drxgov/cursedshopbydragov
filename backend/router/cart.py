from core.security import get_current_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.cart import CartItem
from models.user import User
from schemas.cart import CartItemAdd
from sqlalchemy.orm import Session

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/get_info")
async def get_user_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return db.query(CartItem).filter(CartItem.user_id == current_user.id).all()


@router.post("/add_item")
async def add_item_to_cart(
    item: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == current_user.id, CartItem.product_id == item.product_id
    )
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_item = CartItem(
            user_id=current_user.id, product_id=item.product_id, quantity=item.quantity
        )
        db.add(new_item)
        db.commit()
    return {"message": "товар успешно добавлен в корзину"}


@router.delete("/delete/{product_id}")
async def delete_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id, CartItem.product_id == product_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="товар не найден в корзине")
    db.delete(item)
    db.commit()
    return {"message": "товар успешно удален из корзины"}


@router.delete("/clear")
async def clear_cart(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    return {"message": "корзина успешно очищена"}
