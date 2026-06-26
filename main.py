import os
import uuid

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from context import request_id_var
from crud import (
    create_task,
    create_user,
    delete_task,
    delete_user,
    get_task,
    list_tasks,
    read_user,
    update_task,
    update_user,
)
from database import Base, SessionLocal, engine
from logger import logger
from schemas import TaskCreate, TaskUpdate, UserCreate

# =====================
# LOAD ENV
# =====================

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "tasktracker")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# =====================
# APP
# =====================

app = FastAPI(title=APP_NAME, debug=DEBUG)


# =====================
# MIDDLEWARE
# =====================

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = str(uuid.uuid4())
        token = request_id_var.set(request_id)

        try:
            response = await call_next(request)

            response.headers["X-Request-ID"] = request_id

            logger.info(f"{request.method} {request.url.path}")

            return response

        finally:
            request_id_var.reset(token)


app.add_middleware(RequestLoggingMiddleware)

# =====================
# DATABASE
# =====================

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================
# USER APIs
# =====================

@app.post("/user/create")
def create_user_api(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    logger.info("User CREATE API called")
    return create_user(db, user)


@app.get("/users/{user_id}")
def get_user_api(
    user_id: int,
    db: Session = Depends(get_db),
):
    logger.info("User GET API called")

    user = read_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.put("/users/{user_id}")
def update_user_api(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    logger.info("User UPDATE API called")

    updated = update_user(db, user_id, user)

    if not updated:
        raise HTTPException(status_code=404, detail="User not found")

    return updated


@app.delete("/users/{user_id}")
def delete_user_api(
    user_id: int,
    db: Session = Depends(get_db),
):
    logger.info("User DELETE API called")

    deleted = delete_user(db, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}


# =====================
# TASK APIs
# =====================

@app.post("/tasks/create")
def create_task_api(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    logger.info("Task CREATE API called")
    return create_task(db, task)


@app.get("/tasks/{task_id}")
def get_task_api(
    task_id: int,
    db: Session = Depends(get_db),
):
    logger.info("Task GET API called")

    task = get_task(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.get("/tasks")
def list_tasks_api(
    user_id: int | None = None,
    completed: bool | None = None,
    db: Session = Depends(get_db),
):
    logger.info("Task LIST API called")
    return list_tasks(db, user_id, completed)


@app.put("/tasks/{task_id}")
def update_task_api(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    logger.info("Task UPDATE API called")

    updated = update_task(db, task_id, task)

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated


@app.delete("/tasks/{task_id}")
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
):
    logger.info("Task DELETE API called")

    deleted = delete_task(db, task_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


# =====================
# HEALTH
# =====================

@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="DB not ready",
        )


# =====================
# ROOT
# =====================

@app.get("/")
def root():
    return {"status": "TaskTracker running"}





