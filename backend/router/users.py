from core.dependens import check_admin
from core.security import get_current_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from schemas.user import UserChangeRole, UserRead, UserUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/user_info", response_model=UserRead)
async def get_user_info(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    user_info = db.query(User).filter(User.id == user.id).first()
    if not user_info:
        raise HTTPException(status_code=404, detail="данный юзер не существует")
    return user_info


@router.get("/all_user_info")
async def get_all_users_info(
    db: Session = Depends(get_db), user: User = Depends(check_admin)
):
    user_info = db.query(User).all()
    return user_info


@router.get("/user_info_by_id/{user_id}", response_model=UserRead)
async def get_user_info_by_id(
    user_id: int, db: Session = Depends(get_db), user: User = Depends(check_admin)
):
    user_info = db.query(User).filter(User.id == user_id).first()
    if not user_info:
        raise HTTPException(
            status_code=404, detail="данного пользователя не существует"
        )
    return user_info


@router.patch("/update_user_info")
async def update_user_info(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    existing = db.query(User).filter(User.id == user.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="данного пользоват не существует")
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return {"message": "данные успешно обновлены"}


@router.patch("/change_user_role/{user_id}")
async def change_user_role(
    user_id: int,
    change_role: UserChangeRole,
    db: Session = Depends(get_db),
    user: User = Depends(check_admin),
):
    user_change = db.query(User).filter(User.id == user_id).first()
    if not user_change:
        raise HTTPException(status_code=404, detail="данного пользоват не существует")
    user_change.role = change_role.role
    db.commit()
    return {"message": "роль пользователя успешно обновлена"}
