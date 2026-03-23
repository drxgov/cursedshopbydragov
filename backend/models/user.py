from database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(100), default="buyer")
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="seller")
    cart: Mapped[list["CartItem"]] = relationship(back_populates="user")
