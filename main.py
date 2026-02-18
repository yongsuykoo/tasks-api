from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String(20), default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Models
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: bool = Field(False, description="Task completion status")
    priority: str = Field("medium", pattern="^(low|medium|high)$", description="Task priority")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

class MessageResponse(BaseModel):
    message: str
    id: Optional[int] = None

# FastAPI App
app = FastAPI(
    title="Tasks API",
    description="A complete REST API for managing tasks - Built by Yongskie 🇵🇭",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Tasks API! 🚀",
        "docs": "/docs",
        "endpoints": {
            "list_tasks": "GET /tasks",
            "get_task": "GET /tasks/{id}",
            "create_task": "POST /tasks",
            "update_task": "PUT /tasks/{id}",
            "delete_task": "DELETE /tasks/{id}"
        }
    }

# GET /tasks - List all tasks
@app.get("/tasks", response_model=TaskListResponse, tags=["Tasks"])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieve all tasks with optional filtering."""
    query = db.query(TaskModel)
    
    if completed is not None:
        query = query.filter(TaskModel.completed == completed)
    if priority:
        query = query.filter(TaskModel.priority == priority)
    
    total = query.count()
    tasks = query.offset(skip).limit(limit).all()
    
    return {"tasks": tasks, "total": total}

# GET /tasks/{id} - Get task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific task by ID."""
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    return task

# POST /tasks - Create new task
@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    return db_task

# PUT /tasks/{id} - Update task
@app.put("/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Update an existing task."""
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    
    return db_task

# DELETE /tasks/{id} - Delete task
@app.delete("/tasks/{task_id}", response_model=MessageResponse, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    db.delete(db_task)
    db.commit()
    
    return {"message": f"Task {task_id} deleted successfully", "id": task_id}

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
