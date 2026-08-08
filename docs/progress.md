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


## Session 4 — August 7, 2026

### Completed

- Created `backend/app/services/randomizer_service.py`.
- Added a `generate_pokemon()` function for selecting random Pokémon.
- Configured the randomizer to generate 3 Pokémon by default.
- Used `random.sample()` so generated Pokémon are unique within a result.
- Added validation to prevent requesting more Pokémon than are available.
- Kept the randomization logic separate from the FastAPI route.
- Added a `GET /generate` endpoint.
- Tested the randomizer service independently from FastAPI.
- Verified that repeated calls generate different Pokémon.
- Verified that `/generate` returns 3 unique Pokémon through the browser and FastAPI documentation.
- Reviewed Python type hints and their similarities to Java types.

### Concepts Reviewed

- Separation between API logic and business logic.
- Passing the Pokémon catalog into the randomizer rather than having the randomizer load its own data.
- Python's `random.sample()` function.
- Default function parameters.
- Python type hints:
  - `parameter: Type`
  - `-> ReturnType`
  - `list[Pokemon]`
  - `Path | None`
- Similarities between Python type hints and Java method declarations.
- Python decorators such as `@app.get()` and their conceptual similarity to Java framework annotations.

### Current Project State

- Pokémon data is loaded and validated when the backend starts.
- `GET /pokemon` returns the complete Pokémon catalog.
- `GET /generate` returns 3 unique randomly selected Pokémon.
- Randomization logic is contained in its own service rather than directly inside the API route.

### Next Goal

- Begin adding rules to the randomizer.
- Implement one or both MVP filters:
  - Exclude legendary Pokémon.
  - Restrict generation(s).
- Decide how filter options should be passed from the client to the backend.


## Session 5 — August 8, 2026

### Completed

- Created a `GenerateRequest` Pydantic model for configurable randomization requests.
- Changed the `/generate` endpoint from a fixed GET request to a configurable POST request.
- Added support for:
  - Custom Pokémon count.
  - Generation filtering.
  - Excluding legendary Pokémon.
- Updated the randomizer service to filter the eligible Pokémon pool before random selection.
- Added validation for requests that cannot be satisfied by the available Pokémon.
- Added HTTP error handling to translate randomizer `ValueError` exceptions into `400 Bad Request` responses.
- Verified the distinction between:
  - `200 OK` for successful requests.
  - `400 Bad Request` for valid but impossible randomization requests.
  - `422 Unprocessable Content` for invalid request-model data.
- Installed and configured pytest.
- Created unit tests for the randomizer service.
- Added tests for:
  - Default generation count.
  - Unique Pokémon results.
  - Generation filtering.
  - Legendary exclusion.
  - Requests exceeding the available Pokémon pool.
- Added FastAPI API tests using `TestClient`.
- Added API tests for:
  - Root/status endpoint.
  - Pokémon catalog endpoint.
  - Generation filtering.
  - Unique generated Pokémon.
  - 400 error responses.
  - 422 request validation.
- Established a baseline of 11 passing automated tests.
- Created `pytest.ini` to configure the backend as the Python source root for pytest.
- Added VS Code/Pylance configuration so imports from `app` resolve correctly in test files.
- Separated development dependencies into `requirements-dev.txt`.
- Updated HTTP testing dependencies to remove the TestClient deprecation warning.
- Created an initial PokéAPI import script.
- Successfully retrieved Pokémon and species information from PokéAPI.
- Added an HTTP User-Agent, JSON Accept header, and request timeout to the importer.
- Successfully transformed PokéAPI data for Bulbasaur into the application's simplified Pokémon structure.

### Concepts Reviewed

- REST APIs, routes, endpoints, HTTP methods, request bodies, and responses.
- GET vs. POST requests.
- Path parameters, query parameters, and JSON request bodies.
- HTTP status codes and the distinction between client and server errors.
- Input/model validation vs. business-rule validation.
- Exception handling with `try` / `except`.
- Translating service-layer exceptions into HTTP errors.
- Keeping business logic independent from FastAPI/HTTP concerns.
- Unit tests vs. API/integration-level tests.
- Pytest fixtures and the Arrange → Act → Assert testing pattern.
- Designing randomized tests so randomness cannot hide bugs.
- Runtime imports vs. static analysis/import configuration.
- Production dependencies vs. development dependencies.
- Acting as an HTTP client when consuming an external API.
- HTTP request headers and network timeouts.
- Transforming an external API's data model into our own internal representation.

### Current Project State

- `POST /generate` accepts configurable generation and legendary filters.
- The randomizer validates and handles impossible requests cleanly.
- The backend has 11 passing automated tests covering both service and API behavior.
- A single Pokémon can successfully be retrieved and transformed from PokéAPI.
- The application still uses the small local `pokemon.json` catalog at runtime.
- The PokéAPI importer currently returns a dictionary rather than a validated `Pokemon` model.

### Next Goals

- Decide on a clean project/import structure that allows standalone scripts to reuse backend models.
- Validate imported PokéAPI records using the existing `Pokemon` model.
- Expand the importer from one Pokémon to a larger/full Pokémon catalog.
- Generate `data/pokemon.json` from PokéAPI rather than maintaining it manually.
- Run the existing test suite against the expanded dataset and verify that backend behavior remains unchanged.