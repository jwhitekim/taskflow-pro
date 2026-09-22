from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
from schemas import TaskCreate, TaskUpdate, TaskListItem, TaskDetail

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    has_extra_field = any(error["type"] == "extra_forbidden" for error in exc.errors())
    status_code = 422 if has_extra_field else 400
    return JSONResponse(status_code=status_code, content={"detail": exc.errors()})


@app.post("/api/tasks", response_model=TaskDetail, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/api/tasks", response_model=list[TaskListItem])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.get("/api/tasks/{task_id}", response_model=TaskDetail)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.get(models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.put("/api/tasks/{task_id}", response_model=TaskDetail)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.get(models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in task.model_dump().items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.get(models.Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return None


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
