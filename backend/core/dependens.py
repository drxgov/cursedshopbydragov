from core.security import get_current_user
from fastapi import Depends, HTTPException
from models.user import User


async def check_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="пошел нахуй, ты не админ")
    return user


async def check_seller(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="пошел нахуй, ты не продаец")
    return user
