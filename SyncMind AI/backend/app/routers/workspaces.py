from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.WorkspaceOut)
def create_workspace(payload: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    ws = models.Workspace(name=payload.name)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    return ws


@router.get("/", response_model=list[schemas.WorkspaceOut])
def list_workspaces(db: Session = Depends(get_db)):
    return db.query(models.Workspace).all()

