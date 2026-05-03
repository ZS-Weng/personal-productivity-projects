from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import database as db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class PomoUpdate(BaseModel):
    count: int

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

@app.get("/api/pomos/{date}")
async def get_pomos(date: str):
    return {"date": date, "count": db.get_pomos(date)}

@app.put("/api/pomos/{date}")
async def update_pomos(date: str, body: PomoUpdate):
    count = db.set_pomos(date, body.count)
    return {"date": date, "count": count}

@app.post("/api/pomos/{date}/increment")
async def increment_pomos(date: str):
    count = db.increment_pomos(date)
    return {"date": date, "count": count}

@app.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request):
    return templates.TemplateResponse(name="analytics.html", request=request)

@app.get("/api/pomos")
async def get_all_pomos():
    return db.get_all_pomos()
