from fastapi import FastAPI
from api.routes import users, auth
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}