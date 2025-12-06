from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import engine, Base, get_db
from app.models.model import User
from app.schemas.schema import UserCreate, UserResponse
from app import crud


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user.name, user.email)
    return db_user


@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
