from fastapi import APIRouter, HTTPException
from app.crud.tasks import create_task, get_task, get_tasks, update_task, delete_task
from app.schemas.tasks import TaskCreate, TaskUpdate, Task

router = APIRouter()

@router.post("/", response_model=Task)
async def create_new_task(task: TaskCreate):
    return await create_task(task)

@router.get("/{task_id}", response_model=Task)
async def read_task(task_id: int):
    task = await get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/", response_model=list[Task])
async def read_tasks(skip: int = 0, limit: int = 10):
    return await get_tasks(skip=skip, limit=limit)

@router.put("/{task_id}", response_model=Task)
async def update_existing_task(task_id: int, task: TaskUpdate):
    updated_task = await update_task(task_id, task)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", response_model=dict)
async def delete_existing_task(task_id: int):
    result = await delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}