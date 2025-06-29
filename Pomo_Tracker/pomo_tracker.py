import json
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException, Path as FastApiPath
from pydantic import BaseModel, Field

# --- Configuration & Setup ---

app = FastAPI(
    title="Pomo Tracker API",
    description="A simple API to track Pomodoro sessions for a given month and year.",
    version="1.0.0",
)

# Use Path for a more robust file path handling
DB_FILE = Path("pomo_data.json")

# --- Data Storage Functions ---

def read_db() -> Dict[str, Dict]:
    """Reads the entire Pomodoro database from the JSON file."""
    if not DB_FILE.exists():
        return {}
    try:
        with DB_FILE.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Return empty dict if file is empty or corrupted
        return {}

def write_db(data: Dict[str, Dict]):
    """Writes the entire Pomodoro database to the JSON file."""
    with DB_FILE.open("w") as f:
        json.dump(data, f, indent=4)

# --- Pydantic Models (for data validation and serialization) ---

class PomoUpdate(BaseModel):
    """Data model for updating Pomodoro stats."""
    pomodoros_completed: int = Field(
        ..., ge=0, description="Total number of Pomodoros completed."
    )
    short_breaks: int = Field(
        ..., ge=0, description="Total number of short breaks taken."
    )
    long_breaks: int = Field(
        ..., ge=0, description="Total number of long breaks taken."
    )

class PomoData(PomoUpdate):
    """Data model for representing a month's Pomodoro data in a response."""
    month_key: str = Field(
        ..., description="The year and month key in YYYY-MM format."
    )

# --- API Endpoints ---

@app.get("/", tags=["General"])
async def read_root():
    """A welcome message to the API."""
    return {"message": "Welcome to the Pomo Tracker API!"}

@app.get("/pomo/{year}/{month}", response_model=PomoData, tags=["Pomodoro"])
async def get_pomo_for_month(
    year: int = FastApiPath(..., ge=2020, le=2100, description="The year of the record."),
    month: int = FastApiPath(..., ge=1, le=12, description="The month of the record (1-12).")
):
    """
    Retrieve Pomodoro tracking data for a specific month and year.
    """
    db = read_db()
    month_key = f"{year}-{month:02d}"
    
    if month_key not in db:
        raise HTTPException(
            status_code=404, detail=f"No Pomodoro data found for {month_key}"
        )
    
    pomo_data = db[month_key]
    return PomoData(month_key=month_key, **pomo_data)

@app.put("/pomo/{year}/{month}", response_model=PomoData, tags=["Pomodoro"])
async def update_pomo_for_month(
    pomo_update_data: PomoUpdate,
    year: int = FastApiPath(..., ge=2020, le=2100, description="The year of the record."),
    month: int = FastApiPath(..., ge=1, le=12, description="The month of the record (1-12).")
):
    """
    Create or update the Pomodoro tracking data for a specific month and year.
    
    This endpoint is idempotent: calling it multiple times with the same data
    will result in the same state.
    """
    db = read_db()
    month_key = f"{year}-{month:02d}"
    
    # Update the database with the new data
    db[month_key] = pomo_update_data.model_dump()
    
    write_db(db)
    
    return PomoData(month_key=month_key, **pomo_update_data.model_dump())