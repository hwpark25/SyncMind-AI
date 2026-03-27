from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.get("/project/{project_id}", response_model=list[schemas.TaskOut])
def list_tasks_for_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).get(task_id)
    if not task:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

