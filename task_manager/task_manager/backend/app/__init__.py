# backend/app/__init__.py

from fastapi import FastAPI

app = FastAPI()

from .api.v1.endpoints import tasks  # Importing the tasks endpoints to register them with the app

app.include_router(tasks.router)  # Including the tasks router in the FastAPI application