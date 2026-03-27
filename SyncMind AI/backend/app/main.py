from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import workspaces, transcripts, tasks

app = FastAPI(title="SyncMind AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


app.include_router(workspaces.router, prefix="/api/workspaces", tags=["workspaces"])
app.include_router(transcripts.router, prefix="/api/transcripts", tags=["transcripts"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

