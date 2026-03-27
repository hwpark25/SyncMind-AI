import os
from typing import List

from openai import OpenAI

from .schemas import TaskCreate


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def extract_tasks_from_transcript(project_id: int, transcript_text: str) -> List[TaskCreate]:
    """
    Minimal placeholder around OpenAI API.
    In a real system, you would add robust prompting, schema validation, and error handling.
    """
    if client is None:
        # Fallback: return a single generic task so the pipeline still works locally.
        return [
            TaskCreate(
                project_id=project_id,
                title="Review meeting notes and define action items",
                owner=None,
                due_date=None,
                status="pending",
                source_transcript_id=None,
            )
        ]

    prompt = (
        "You are an assistant that extracts concrete, student-team-friendly action items from meeting transcripts.\n"
        "Given the transcript below, list 3-7 action items with: title, optional owner (name), "
        "and optional due date (YYYY-MM-DD) when clearly implied.\n\n"
        f"Transcript:\n{transcript_text}\n"
    )

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    text = response.output[0].content[0].text.value  # Simplified; you might want JSON in production

    # Very naive parsing – the goal here is to keep the example lightweight.
    lines = [line.strip("-• ").strip() for line in text.splitlines() if line.strip()]
    tasks: List[TaskCreate] = []
    for line in lines:
        if not line:
            continue
        tasks.append(
            TaskCreate(
                project_id=project_id,
                title=line,
                owner=None,
                due_date=None,
                status="pending",
                source_transcript_id=None,
            )
        )

    if not tasks:
        tasks.append(
            TaskCreate(
                project_id=project_id,
                title="Review meeting notes and define action items",
                owner=None,
                due_date=None,
                status="pending",
                source_transcript_id=None,
            )
        )

    return tasks

