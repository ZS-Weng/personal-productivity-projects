from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional
import os

# Import our database components
from database import SessionLocal, engine, get_db, Base
from models import PomodoroSession

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Pomodoro Timer App", version="1.0.0")

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/save-pomodoros")
async def save_pomodoros(
    pomodoros: int = Form(...),
    year: int = Form(...),
    month: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Save completed pomodoros to database for a specific year and month
    """
    try:
        # Create new pomodoro session
        new_session = PomodoroSession(
            pomodoros_completed=pomodoros,
            year=year,
            month=month
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return {
            "success": True,
            "message": f"Saved {pomodoros} pomodoros for {month}/{year}",
            "session_id": new_session.id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving pomodoros: {str(e)}")

@app.get("/api/stats")
async def get_stats(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get pomodoro statistics
    """
    try:
        # Build query
        query = db.query(PomodoroSession)
        
        if year:
            query = query.filter(PomodoroSession.year == year)
        if month:
            query = query.filter(PomodoroSession.month == month)
        
        # Get all sessions
        sessions = query.all()
        
        # Calculate totals
        total_pomodoros = sum(session.pomodoros_completed for session in sessions)
        total_sessions = len(sessions)
        
        # Get monthly breakdown for current year if no specific filters
        monthly_breakdown = []
        if not year and not month:
            current_year = datetime.now().year
            monthly_data = db.query(
                PomodoroSession.month,
                func.sum(PomodoroSession.pomodoros_completed).label('total')
            ).filter(
                PomodoroSession.year == current_year
            ).group_by(PomodoroSession.month).all()
            
            monthly_breakdown = [
                {"month": month, "total": total}
                for month, total in monthly_data
            ]
        
        return {
            "total_pomodoros": total_pomodoros,
            "total_sessions": total_sessions,
            "monthly_breakdown": monthly_breakdown,
            "filters": {
                "year": year,
                "month": month
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@app.get("/api/years")
async def get_available_years(db: Session = Depends(get_db)):
    """
    Get all years that have pomodoro data
    """
    try:
        years = db.query(PomodoroSession.year).distinct().order_by(PomodoroSession.year.desc()).all()
        return {"years": [year[0] for year in years]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting years: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)