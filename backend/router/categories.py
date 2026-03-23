from core.dependens import check_admin
from core.security import get_current_user
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.categories import Category
from models.products import Product
from models.user import User
from schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/category", tags=["categories"])


@router.get("/get_info")
async def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.post("/create")
async def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(check_admin),
):
    existing = db.query(Category).filter(Category.title == category.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="данная категория уже существует")
    new_category = Category(title=category.title, description=category.description)
    db.add(new_category)
    db.commit()
    return {"message": "категория успешно создана"}


@router.get("/get_by_id/{category_id}", response_model=CategoryRead)
async def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="категория не найдена")
    return category


@router.delete("/delete/{category_id}")
async def delete_category(
    category_id: int, db: Session = Depends(get_db), user: User = Depends(check_admin)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="данная категория не найдена")
    db.delete(category)
    db.commit()
    return {"message": "категория успешно удалена"}


@router.patch("/update/{category_id}")
async def update_category(
    category_id: int,
    categoryupdate: CategoryUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(check_admin),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="категория не найдена")
    update_data = categoryupdate.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return {"message": "категория успешно обновлена", "category": category}
