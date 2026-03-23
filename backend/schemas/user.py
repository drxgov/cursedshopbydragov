from cmath import e

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class UserChangeRole(BaseModel):
    role: str
