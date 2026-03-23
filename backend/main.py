from fastapi import FastAPI
from models.categories import Category
from models.products import Product
from models.user import User
from router.auth import router as auth_router
from router.categories import router as categories_router
from router.products import router as product_router
from router.users import router as users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(product_router)
app.include_router(users_router)


@app.get("/")
async def get_root():
    return {"message": "good"}
