from core.security import create_access_token, hash_password, verify_password
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from schemas.user import UserCreate, UserLogin
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth/register"])


@router.post("/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(
            status_code=401, detail="пользователь с таким email уже существует"
        )
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    return {"message": "пользователь успешно создан"}


@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    xuser = db.query(User).filter(User.email == user.email).first()
    if not user or not verify_password(user.password, xuser.hashed_password):
        raise HTTPException(status_code=401, detail="неверная почта или пароль")
    token = create_access_token({"sub": str(xuser.id)})
    return token
