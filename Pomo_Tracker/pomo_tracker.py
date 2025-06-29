import json
from pathlib import Path
from typing import Dict
import datetime

from fastapi import FastAPI, HTTPException, Path as FastApiPath
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse

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

@app.get("/", response_class=HTMLResponse, tags=["General"])
async def home_interface():
    """
    Provides a simple HTML interface to select a year and month to view Pomodoro data.
    """
    current_year = datetime.datetime.now().year
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pomo Tracker</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f9; color: #333; }}
            .container {{ max-width: 600px; margin: 40px auto; padding: 20px; }}
            h1 {{ color: #2c3e50; text-align: center; }}
            #pomoForm {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            .form-group {{ margin-bottom: 15px; }}
            label {{ font-weight: bold; display: block; margin-bottom: 5px; }}
            select, input, button {{ width: 100%; box-sizing: border-box; padding: 10px; margin-top: 5px; border-radius: 4px; border: 1px solid #ddd; font-size: 16px; }}
            button {{ background-color: #3498db; color: white; border: none; cursor: pointer; font-weight: bold; transition: background-color 0.2s; }}
            button:hover {{ background-color: #2980b9; }}
            #results {{ padding: 20px; background: #e9ecef; border-radius: 8px; min-height: 50px; }}
            #results h3 {{ margin-top: 0; color: #34495e; }}
            #results ul {{ padding-left: 20px; list-style-type: none; }}
            #results li {{ margin-bottom: 10px; }}
            .error {{ color: #e74c3c; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Pomo Tracker</h1>
            <form id="pomoForm">
                <div class="form-group">
                    <label for="year">Year:</label>
                    <input type="number" id="year" name="year" value="{current_year}" required>
                </div>
                <div class="form-group">
                    <label for="month">Month:</label>
                    <select id="month" name="month" required>
                        <option value="1">January</option><option value="2">February</option><option value="3">March</option>
                        <option value="4">April</option><option value="5">May</option><option value="6">June</option>
                        <option value="7">July</option><option value="8">August</option><option value="9">September</option>
                        <option value="10">October</option><option value="11">November</option><option value="12">December</option>
                    </select>
                </div>
                <button type="submit">Get Pomo Data</button>
            </form>

            <div id="results">
                <p>Select a year and month to see your stats.</p>
            </div>
        </div>

        <script>
            document.getElementById('pomoForm').addEventListener('submit', async function (e) {{
                e.preventDefault();
                const year = document.getElementById('year').value;
                const month = document.getElementById('month').value;
                const resultsDiv = document.getElementById('results');
                
                resultsDiv.innerHTML = '<p>Loading...</p>';

                try {{
                    const response = await fetch(`/pomo/${{year}}/${{month}}`);
                    if (response.ok) {{
                        const data = await response.json();
                        resultsDiv.innerHTML = `
                            <h3>Stats for ${{data.month_key}}</h3>
                            <ul>
                                <li><strong>Pomodoros Completed:</strong> ${{data.pomodoros_completed}}</li>
                                <li><strong>Short Breaks:</strong> ${{data.short_breaks}}</li>
                                <li><strong>Long Breaks:</strong> ${{data.long_breaks}}</li>
                            </ul>`;
                    }} else {{
                        const errorData = await response.json();
                        resultsDiv.innerHTML = `<p class="error">${{errorData.detail || 'An unexpected error occurred.'}}</p>`;
                    }}
                }} catch (error) {{
                    resultsDiv.innerHTML = `<p class="error">Failed to fetch data. Is the API server running?</p>`;
                }}
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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