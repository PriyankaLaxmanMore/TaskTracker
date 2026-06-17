from sqlalchemy.orm import Session
from model import User
from schemas import *
from fastapi import FastAPI, Depends, HTTPException

def create_user(db: Session,user:userCreate):
    db_user=User(name=user.name,email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user_data):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    # update fields
    if user_data.name is not None:
        db_user.name = user_data.name

    if user_data.email is not None:
        db_user.email = user_data.email

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user