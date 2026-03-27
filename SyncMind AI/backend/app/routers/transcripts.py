from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, llm
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.TranscriptOut)
def ingest_transcript(payload: schemas.TranscriptCreate, db: Session = Depends(get_db)):
    transcript = models.Transcript(project_id=payload.project_id, raw_text=payload.raw_text)
    db.add(transcript)
    db.commit()
    db.refresh(transcript)
    return transcript


@router.post("/{transcript_id}/generate-tasks", response_model=list[schemas.TaskOut])
def generate_tasks_from_transcript(transcript_id: int, db: Session = Depends(get_db)):
    transcript = db.query(models.Transcript).get(transcript_id)
    if not transcript:
        return []

    task_creates = llm.extract_tasks_from_transcript(
        project_id=transcript.project_id,
        transcript_text=transcript.raw_text,
    )

    created_tasks = []
    for t in task_creates:
        task = models.Task(
            project_id=t.project_id,
            title=t.title,
            owner=t.owner,
            due_date=t.due_date,
            status=t.status,
            source_transcript_id=transcript.id,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        created_tasks.append(task)

    return created_tasks

