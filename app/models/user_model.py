from sqlalchemy import Column, Integer, String
from core.database import Base
from pydantic import BaseModel, EmailStr, Field

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String, nullable=False)

class UserBase(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
