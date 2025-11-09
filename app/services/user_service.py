from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate

def create_user(db: Session, user_data: UserCreate):
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = user_data.name
        user.email = user_data.email
        db.commit()
        db.refresh(user)
        return user
    return None


def list_users(db: Session):
    return db.query(User).all()


