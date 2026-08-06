## Session 1 - August 1, 2026

### Completed
- Setup project repository
- Connected to git and github
- Commited and pushed project file structure to github

### Next Goals
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


## Session 3 — August 6, 2026

### Completed

- Created a small local Pokémon dataset in `data/pokemon.json`.
- Added Pokémon from Generations 1–3, including Mewtwo as a legendary test case.
- Validated the JSON file using Python's built-in JSON tool.
- Created a `Pokemon` Pydantic model in `backend/app/models/pokemon.py`.
- Defined the fields required for each Pokémon:
  - `pokedex_number`
  - `name`
  - `generation`
  - `types`
  - `is_legendary`
- Tested the Pokémon model with both valid and invalid input.
- Created a Pokémon loader service in `backend/app/services/pokemon_loader.py`.
- Used `pathlib.Path` to locate the Pokémon data file reliably.
- Added support for supplying an alternate data file path for future testing.
- Converted raw JSON dictionaries into validated `Pokemon` objects.
- Added a `GET /pokemon` API endpoint.
- Configured FastAPI to return a list of Pokémon using the `Pokemon` response model.
- Verified that `/pokemon` returns all Pokémon in the dataset.
- Verified that FastAPI's `/docs` page displays the Pokémon response schema.
- Renamed the generic `id` field to `pokedex_number` to better describe its meaning.

### Concepts Reviewed

- Organizing Python code into packages and modules.
- Similarities between Python models and Java classes, DTOs, or records.
- Difference between raw JSON data and validated application objects.
- Purpose of Pydantic models.
- Purpose of a service or data-loading layer.
- Dictionary unpacking and Pydantic model validation.
- Separation of responsibilities between:
  - Data storage
  - Data models
  - Loader services
  - API endpoints
- Difference between an application's internal data structure and PokéAPI's external response structure.
- Benefits of descriptive field names such as `pokedex_number`.

### Current Project State

- The backend loads Pokémon data when the application starts.
- The dataset is validated against the `Pokemon` model.
- `GET /pokemon` returns the complete Pokémon catalog.
- The API documentation displays the expected Pokémon schema.

### Next Goal

- Create a randomizer service.
- Add a `GET /generate` endpoint that returns three unique random Pokémon.
- Begin separating randomization rules from the API route.