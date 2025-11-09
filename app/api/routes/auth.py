from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from core.database import get_db
from core.security import create_access_token, verify_password
from models.user_model import User
from schemas.user_schema import Token
from core.config import settings

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    # Adiciona a verificação do tamanho da senha
    if len(form_data.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password is too long",
        )
    
    print(f"Attempting login for user: {form_data.username}") # Adicione esta linha

    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        print("User not found in database.") # Adicione esta linha
    elif not verify_password(form_data.password, user.hashed_password):
        print("Password verification failed.") # Adicione esta linha

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}