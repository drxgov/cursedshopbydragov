from core.dependens import check_seller
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.categories import Category
from models.products import Product
from models.user import User
from schemas.products import ProductCreate, ProductUpdate
from sqlalchemy.orm import Session

router = APIRouter(prefix="/product", tags=["Products"])


@router.get("/get_all")
async def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="товаров не найдено")
    return products


@router.post("/create")
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(check_seller),
):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="данной категории не существует")
    new_product = Product(**product.model_dump(), seller_id=current_user.id)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "товар успешно создан", "product": new_product}


@router.get("/get_by_id/{product_id}")
async def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="данный товар не найден")
    return product


@router.get("/get_by_seller_id/{seller_id}")
async def get_product_by_seller_id(seller_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.seller_id == seller_id).all()
    if not product:
        raise HTTPException(
            status_code=404, detail="у данного продавца отсутсвуют товары"
        )
    return product


@router.get("/get_by_category_id/{category_id}")
async def get_product_by_category_id(category_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.category_id == category_id).all()
    if not product:
        raise HTTPException(
            status_code=404, detail="в данной категории отсутсвуют товары"
        )
    return product


@router.delete("/delete/{product_id}")
async def delete_product(
    product_id: int, db: Session = Depends(get_db), user: User = Depends(check_seller)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="данный товар не найден")
    db.delete(product)
    db.commit()
    return {"message": "данный товар удален"}


@router.patch("/update/{product_id}")
async def update_product(
    product_id: int,
    product_up: ProductUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(check_seller),
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.seller_id == user.id)
        .first()
    )
    if not product:
        raise HTTPException(
            status_code=404, detail="данный товар не найден или не принадлежит вам"
        )
    update_data = product_up.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return {"message": "успешно обновлены данный о товаре", "product": product}
