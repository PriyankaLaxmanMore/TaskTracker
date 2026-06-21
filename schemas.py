from pydantic import BaseModel

# =====================
# USER SCHEMAS
# =====================


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# =====================
# TASK SCHEMAS
# =====================


class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    user_id: int
    completed: bool

    class Config:
        from_attributes = True
