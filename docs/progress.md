# Session 1 - August 1, 2026

## Completed
- Setup project repository
- Connected to git and github
- Commited and pushed project file structure to github

## Next Goals
- Begin building backend
- Setup FastAPI (?)

## Session 2 — August 5, 2026

### Completed

- Reviewed why Pokémon generation and filtering logic should live in the backend rather than the frontend.
- Documented the planned backend responsibilities and API endpoints.
- Created a Python virtual environment inside `backend/.venv`.
- Learned why virtual environments should not be committed to Git.
- Added `.venv`, Python cache files, and compiled Python files to `.gitignore`.
- Activated the virtual environment in PowerShell.
- Temporarily adjusted the PowerShell execution policy so the activation script could run.
- Installed FastAPI and Uvicorn inside the virtual environment.
- Generated `backend/requirements.txt` to record the Python dependencies.
- Created the initial backend application structure:
  - `backend/app/__init__.py`
  - `backend/app/main.py`
- Created the first FastAPI endpoint at `GET /`.
- Ran the backend locally using Uvicorn with automatic reload enabled.
- Configured VS Code to use the Python interpreter from `backend/.venv`.
- Committed and pushed the initial FastAPI backend setup to GitHub.

### Concepts Reviewed

- Difference between frontend presentation logic and backend business logic.
- Separation of responsibilities between the API, randomizer service, repository, and data source.
- Difference between FastAPI and Uvicorn.
- Purpose of Python virtual environments.
- Difference between `.venv` and `requirements.txt`.
- How `.gitignore` prevents generated and machine-specific files from being committed.
- Basic FastAPI routes, decorators, and JSON responses.

### Current Project State

- The Git repository is clean and synchronized with `origin/main`.
- The backend server can be started locally.
- The API currently returns a basic status message confirming that it is running.

### Next Goal

- Create a small local Pokémon dataset.
- Define how a Pokémon should be represented in the backend.
- Load the Pokémon data into the application.

