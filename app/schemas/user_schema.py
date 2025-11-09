from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=100)

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
