from fastapi import FastAPI,Depends
from database import *
from schemas import userCreate
from sqlalchemy.orm import Session
from crud import *


app=FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally :
        db.close()

@app.post("/user/create")
async def create_user_api(user: userCreate,db:Session=Depends(get_db)) :
    return create_user(db, user)

# GET USER BY ID
@app.get("/users/{user_id}")
async def get_user_api(user_id: int, db: Session = Depends(get_db)):
    user = read_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@app.put("/users/{user_id}")
async def update_user_api(
    user_id: int,
    user: userCreate,
    db: Session = Depends(get_db)
):
    updated_user = update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

@app.delete("/users/{user_id}")
async def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)

    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}