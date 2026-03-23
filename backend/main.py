from database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.cart import CartItem
from models.categories import Category
from models.products import Product
from models.user import User
from router.auth import router as auth_router
from router.cart import router as cart_router
from router.categories import router as categories_router
from router.products import router as product_router
from router.users import router as users_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(product_router)
app.include_router(users_router)
app.include_router(cart_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def get_root():
    return {"message": "good"}
