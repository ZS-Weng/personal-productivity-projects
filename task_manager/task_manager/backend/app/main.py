from fastapi import FastAPI
from app.api.v1.endpoints import tasks

app = FastAPI()

app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}