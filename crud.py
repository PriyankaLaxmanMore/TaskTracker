from sqlalchemy.orm import Session
from model import User, Task
from schemas import UserCreate, TaskCreate, TaskUpdate

# =====================
# USER CRUD
# =====================


def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = read_user(db, user_id)
    if not db_user:
        return None

    db_user.name = user_data.name
    db_user.email = user_data.email

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = read_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


# =====================
# TASK CRUD
# =====================


def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        completed=False,
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(db: Session, user_id: int = None, completed: bool = None):
    query = db.query(Task)

    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    return query.all()


def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    if task.title is not None:
        db_task.title = task.title

    if task.description is not None:
        db_task.description = task.description

    if task.user_id is not None:
        db_task.user_id = task.user_id

    if task.completed is not None:
        db_task.completed = task.completed

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    db.delete(db_task)
    db.commit()
    return db_task
