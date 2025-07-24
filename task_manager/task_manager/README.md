# Task Manager

This project is a task management application that consists of a backend built with FastAPI and a frontend developed using Svelte. 

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

### Backend

The backend is responsible for handling API requests, managing the database, and processing business logic. It is structured as follows:

- `app/`: Contains the main application code.
  - `__init__.py`: Initializes the app package.
  - `main.py`: Entry point for the backend application.
  - `core/`: Contains core functionalities such as configuration and database management.
    - `config.py`: Configuration settings for the application.
    - `database.py`: Database connection and session management.
  - `crud/`: Contains functions for interacting with the database.
    - `tasks.py`: CRUD operations for tasks.
  - `models/`: Defines the data models for the application.
    - `tasks.py`: Data models for tasks.
  - `schemas/`: Defines Pydantic schemas for data validation.
    - `tasks.py`: Schemas for task data.
  - `api/`: Contains the API endpoints.
    - `v1/`: Version 1 of the API.
      - `endpoints/`: Contains the route handlers.
        - `tasks.py`: API endpoints related to tasks.
- `requirements.txt`: Lists the dependencies required for the backend.
- `.env`: Contains environment variables for the application.

### Frontend

The frontend is responsible for the user interface and user experience. It is structured as follows:

- `public/`: Contains static files.
  - `index.html`: Main HTML file for the Svelte application.
- `src/`: Contains the source code for the frontend application.
  - `App.svelte`: Main Svelte component.
  - `main.js`: Initializes and mounts the Svelte application.
  - `components/`: Contains reusable Svelte components.
    - `TaskItem.svelte`: Component for displaying individual tasks.
    - `TaskForm.svelte`: Component for creating and editing tasks.
  - `stores/`: Contains Svelte stores for state management.
    - `taskStore.js`: Store for managing task state.
  - `lib/`: Contains utility functions.
    - `api.js`: Functions for making API calls to the backend.
- `package.json`: Configuration file for npm.
- `svelte.config.js`: Configuration settings for Svelte.
- `vite.config.js`: Configuration settings for Vite.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd task_manager
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Create a virtual environment and activate it.
   - Install the required dependencies:
     ```
     pip install -r requirements.txt
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install the required dependencies:
     ```
     npm install
     ```

4. Run the applications:
   - Start the backend server:
     ```
     uvicorn app.main:app --reload
     ```
   - Start the frontend development server:
     ```
     npm run dev
     ```

## Usage

Once both the backend and frontend are running, you can access the application in your web browser at `http://localhost:3000`. You can create, read, update, and delete tasks through the user interface.