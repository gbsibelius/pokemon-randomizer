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


## Session 6 — August 9, 2026

### Completed

- Moved the PokéAPI importer from the top-level `scripts/` directory into the backend application under `backend/app/tools/`.
- Added `backend/app/tools/__init__.py` so the tools directory is part of the backend Python package structure.
- Updated the importer to reuse the existing `Pokemon` Pydantic model.
- Changed `import_pokemon()` to return a validated `Pokemon` object instead of an unvalidated dictionary.
- Updated JSON output to use `Pokemon.model_dump()` before serialization.
- Changed the importer to run as a Python module using:
  - `python -m app.tools.import_pokemon`
- Verified that PokéAPI data for Bulbasaur is successfully transformed into a validated `Pokemon` object.
- Removed the temporary type-checking print statement after verifying the importer returned the expected model type.
- Added `tests/test_import_pokemon.py`.
- Added a deterministic unit test for `get_generation_number()`.
- Verified the complete automated test suite passes with 12 tests.

### Concepts Reviewed

- Python packages versus standalone scripts.
- Why application tooling should reuse existing domain models instead of defining its own data structure.
- Benefits of validating external API data before adding it to the application dataset.
- Running Python package modules with `python -m`.
- Converting Pydantic models into dictionaries using `model_dump()`.
- Why normal unit tests should avoid depending directly on external network services.
- Difference between testing our transformation logic and testing whether PokéAPI happens to be available.
- Introduction to the idea of mocking external HTTP dependencies for future tests.

### Current Project State

- PokéAPI data can be retrieved and transformed into the application's internal Pokémon representation.
- Imported Pokémon are now validated using the same `Pokemon` model used by the backend.
- The importer is integrated into the backend's package structure.
- The application still uses the small existing `data/pokemon.json` catalog at runtime.
- The test suite currently contains 12 passing tests.

### Next Goals

- Learn how to mock PokéAPI responses so the full importer can be tested without making real network requests.
- Add automated tests for the complete PokéAPI-to-`Pokemon` transformation.
- Expand the importer to retrieve multiple Pokémon.
- Eventually generate the full `data/pokemon.json` dataset automatically.


## Session 7 — August 11, 2026

### Completed

- Added full PokéAPI transformation testing using mocked API responses.
- Improved Pokémon name handling by using PokéAPI's English display names.
- Updated the importer to follow each species' default variety rather than assuming the Pokémon endpoint matches the species ID directly.
- Added batch importing with `import_pokedex()`.
- Added automated tests for batch importing.
- Added support for distinguishing Legendary and Mythical Pokémon.
- Updated the `Pokemon` model with:
  - `is_legendary`
  - `is_mythical`
- Updated importer tests, randomizer fixtures, API expectations, and local dataset schema for the Legendary/Mythical distinction.
- Added JSON-writing support for imported Pokémon.
- Added round-trip testing to verify generated JSON can be loaded back through `pokemon_loader`.
- Added dynamic Pokédex discovery using PokéAPI pagination rather than hardcoding the final Pokédex number.
- Added a reusable PokéAPI resource-ID parser.
- Added tests for pagination and Pokédex discovery.
- Added import progress reporting.
- Added HTTP retry handling for temporary network failures and timeouts.
- Successfully verified retry behavior during a real batch import.
- Added all six Pokémon base stats to the application model:
  - HP
  - Attack
  - Defense
  - Special Attack
  - Special Defense
  - Speed
- Added stat extraction from PokéAPI without requiring additional API requests.
- Added automated tests for base-stat transformation.
- Migrated existing tests and local Pokémon data to the expanded model.
- Added Pokédex integrity validation.
- Added tests for valid and incomplete Pokédex datasets.
- Successfully discovered all 1,025 species from PokéAPI.
- Successfully imported all 1,025 Pokémon species using their default varieties.
- Generated a full local Pokédex JSON dataset.
- Loaded and validated all 1,025 generated records through the existing `pokemon_loader`.
- Promoted the generated dataset to `data/pokemon.json`.
- Verified the full test suite passes with 19 tests.
- Verified FastAPI starts correctly and serves the full generated Pokédex.

### Concepts Reviewed

- Mocking external dependencies with pytest `monkeypatch`.
- Unit-test boundaries and mocking the dependency immediately below the unit under test.
- Python list comprehensions and their relationship to traditional loops and Java streams.
- Batch processing and orchestration.
- Python `enumerate()`, `range()`, list slicing, `append()`, and `extend()`.
- Separating external API schemas from internal application models.
- Default Pokémon varieties versus Pokémon species.
- Data-schema migrations and how model changes affect stored JSON and tests.
- Difference between pytest collection errors and normal test failures.
- JSON serialization and deserialization.
- Temporary filesystem testing with pytest `tmp_path`.
- API pagination.
- HTTP retries, timeouts, and transient versus non-transient failures.
- Derived data versus stored data, particularly BST versus individual base stats.
- Build-time/data-import dependencies versus runtime application dependencies.
- Dataset integrity validation before promoting generated data into production use.

### Current Project State

- The backend uses a generated local dataset containing 1,025 Pokémon species.
- Each Pokémon currently represents its default PokéAPI variety.
- Each record contains:
  - National Pokédex number
  - English display name
  - Generation
  - Type(s)
  - HP
  - Attack
  - Defense
  - Special Attack
  - Special Defense
  - Speed
  - Legendary status
  - Mythical status
- The application does not depend on PokéAPI during normal runtime.
- PokéAPI is only required when regenerating or updating the local dataset.
- The randomizer continues to support generation filtering and Legendary exclusion.
- The FastAPI application successfully loads and serves the full dataset.
- The automated test suite contains 19 passing tests.

### Next Goals

- Add independent Mythical exclusion support to generation requests.
- Add BST-based filtering using the six stored base stats.
- Consider exposing individual stat filters in the future.
- Decide how alternate Pokémon varieties/forms should be represented in the randomization pool.
- Revisit Pokémon identity before adding variants, likely separating National Pokédex species number from a variety-specific identifier.
- Eventually begin frontend development once the desired MVP backend filtering behavior is settled.


## Session 8 — August 12, 2026

### Completed

- Added independent Mythical Pokémon exclusion support.
- Updated `GenerateRequest`, the randomizer service, and the `/generate` API endpoint to support `exclude_mythicals`.
- Added service and API tests for Mythical exclusion.
- Added a computed `bst` property to the `Pokemon` model using the six stored base stats.
- Added optional minimum and maximum BST filters to generation requests.
- Added cross-field validation to reject requests where `min_bst` is greater than `max_bst`.
- Added randomizer service tests for:
  - Minimum BST filtering.
  - Maximum BST filtering.
  - Combined BST range filtering.
- Updated the randomizer test fixture to use real Pokémon base stats rather than placeholder values.
- Added API tests for:
  - BST filtering.
  - Invalid BST ranges.
  - Mythical exclusion.
- Expanded the `/pokemon` API contract test to include all six base stat fields.
- Installed and configured `pytest-cov`.
- Ran line and branch coverage through pytest and VS Code.
- Achieved full line/branch coverage for the core randomizer service, request model, Pokémon model, and API layer.
- Added a missing loader failure-path test for non-array JSON data, bringing `pokemon_loader` to full branch coverage.
- Installed Node.js and npm for frontend development.
- Created the frontend using React, TypeScript, and Vite.
- Selected ESLint for frontend linting.
- Learned the basic frontend project structure, including:
  - `index.html`
  - `main.tsx`
  - `App.tsx`
  - CSS files
  - `package.json`
  - `node_modules`
  - TypeScript/Vite configuration
- Replaced the default Vite starter interface with the first Pokémon Randomizer UI.
- Added basic React state and event handling.
- Added FastAPI CORS configuration for the local React development server.
- Created a TypeScript `Pokemon` interface matching the backend API response.
- Replaced the temporary click counter with a real HTTP `POST /generate` request.
- Connected the React frontend to the FastAPI backend.
- Displayed three randomly generated Pokémon in the browser with:
  - Name
  - Type(s)
  - Generation
- Verified repeated clicks generate new Pokémon without refreshing the page.

### Concepts Reviewed

- Frontend versus backend responsibilities.
- HTML as webpage structure.
- CSS as presentation and styling.
- TypeScript/JavaScript as frontend behavior.
- React components and JSX.
- React state with `useState`.
- Event handlers and `onClick`.
- JSX expressions using `{}`.
- Rendering arrays with `.map()`.
- TypeScript interfaces.
- Asynchronous functions and `await`.
- Browser `fetch()` requests.
- JSON serialization with `JSON.stringify()`.
- CORS and browser origin security.
- Vite's development server and Hot Module Replacement.
- Node.js versus npm.
- `package.json`, `package-lock.json`, and `node_modules`.
- Frontend development server versus production builds.
- Line coverage versus branch coverage.
- Using code coverage as a gap detector rather than simply targeting 100%.

### Current Project State

- Backend uses the complete locally stored 1,025-species Pokémon dataset.
- Generation supports:
  - Custom Pokémon count.
  - Generation filtering.
  - Legendary exclusion.
  - Mythical exclusion.
  - Minimum BST.
  - Maximum BST.
- Invalid BST ranges are rejected during request validation.
- Core runtime backend code has strong line and branch test coverage.
- React + TypeScript frontend is running through Vite.
- The frontend successfully communicates with FastAPI.
- Clicking `Generate Pokémon` retrieves and displays three real randomized Pokémon.
- The frontend currently displays Pokémon names, types, and generations.
- Filter controls have not yet been added to the frontend.
- Pokémon cards are functional placeholders and have not yet received final visual design.

### Next Goals

- Begin designing the actual Pokémon result cards.
- Decide how Pokémon artwork/images should be sourced and represented.
- Create frontend filter controls for:
  - Generations.
  - Legendary exclusion.
  - Mythical exclusion.
  - BST range.
- Connect those controls to the existing `/generate` request.
- Add frontend loading and error states.
- Refactor `App.tsx` into smaller React components as the interface grows.
- Explore responsive/mobile-friendly layout.
- Eventually revisit alternate Pokémon varieties/forms as a separate data-model milestone.


## Session 9 — August 14, 2026

### Completed

- Added frontend controls for excluding Legendary Pokémon.
- Added frontend controls for excluding Mythical Pokémon.
- Connected both exclusion controls to the existing `/generate` API request.
- Verified Legendary and Mythical filters work through the complete frontend-to-backend flow.
- Added generation selection controls for Generations 1 through 9.
- Added React state for tracking selected generations.
- Added generation toggle behavior for selecting and deselecting multiple generations.
- Connected selected generations to the `/generate` request.
- Preserved the backend's existing behavior where no selected generations means no generation restriction.
- Verified generation filtering works individually and in combination with Legendary/Mythical exclusion.
- Identified Ultra Beasts as a potential future filter category.

### Concepts Reviewed

- Controlled form inputs in React.
- Checkbox state using `checked` and `onChange`.
- React state for boolean values and arrays.
- Updating array state immutably.
- JavaScript/TypeScript `.includes()`, `.filter()`, and spread syntax.
- Rendering repeated form controls with `.map()`.
- HTML `fieldset`, `legend`, `label`, and checkbox inputs.
- Conditional request values using the ternary operator.
- Combining multiple frontend filters into a single API request.
- Responsive wrapping of frontend controls using CSS flexbox.

### Current Project State

- React frontend communicates successfully with FastAPI.
- Clicking Generate displays three randomized Pokémon.
- Frontend generation requests currently support:
  - Generation selection.
  - Legendary exclusion.
  - Mythical exclusion.
- Multiple generations can be selected simultaneously.
- Selecting no generations allows Pokémon from every generation.
- Backend BST filtering exists but does not yet have frontend controls.
- Result cards currently display Pokémon name, type(s), and generation.
- Pokémon result-card styling is still an early placeholder.

### Next Goals

- Add frontend minimum and maximum BST controls.
- Add loading and error states for generation requests.
- Begin refining the Pokémon result-card design.
- Decide how Pokémon artwork should be sourced and displayed.
- Refactor the growing `App.tsx` into smaller React components.
- Investigate adding Ultra Beast metadata/filtering in a future backend/data-model update.


## Session 10 — August 15, 2026

### Completed

- Added minimum and maximum BST controls to the React frontend.
- Added React state for optional BST bounds.
- Converted browser number-input values into `number | null` application state.
- Connected `min_bst` and `max_bst` to the `/generate` request.
- Added frontend BST calculation using the six base stats returned by the API.
- Added stat displays for:
  - HP
  - Attack
  - Defense
  - Special Attack
  - Special Defense
  - Speed
  - BST
- Verified BST filtering visually using displayed BST values.
- Added request loading state.
- Disabled the Generate button while a request is in progress.
- Added frontend error state and error-message rendering.
- Added explicit handling for unsuccessful HTTP responses using `response.ok`.
- Added `try` / `catch` / `finally` handling around generation requests.
- Verified an invalid BST range produces a graceful frontend error.
- Verified stopping FastAPI produces a network failure message without breaking the page.
- Preserved previously generated Pokémon when a new request fails.

### Concepts Reviewed

- Controlled numeric inputs in React.
- Translating between browser string values and application numeric/null state.
- The nullish coalescing operator (`??`).
- JavaScript `Number(...)` conversion.
- Derived frontend data.
- Rendering stat collections with `.map()`.
- TypeScript type inference inside array mapping.
- `async` / `await`.
- `try` / `catch` / `finally`.
- `response.ok`.
- Difference between HTTP errors and network failures.
- Conditional rendering.
- Loading state and disabling controls during requests.
- Backend-authoritative validation versus frontend UX validation.

### Current Project State

- Frontend supports:
  - Generation filtering.
  - Legendary exclusion.
  - Mythical exclusion.
  - Minimum BST.
  - Maximum BST.
- Result cards display:
  - Pokémon name
  - Type(s)
  - Generation
  - All six base stats
  - BST
- Generation requests now handle loading and failure states gracefully.
- Backend validation remains authoritative.
- Frontend currently shows a generic API error for invalid requests.
- Network failures show the browser-generated fetch error.
- Result-card styling is still intentionally basic.

### Next Goals

- Refactor the growing `App.tsx` into smaller components.
- Improve API error parsing so backend validation messages can be shown to the user.
- Begin deliberate visual design of the Pokémon cards and filter panel.
- Decide how Pokémon artwork/images should be sourced.
- Consider frontend validation for invalid BST ranges.
- Investigate Ultra Beast metadata/filtering as a later backend/data-model feature.


## Session 11 — August 16, 2026

### Completed

- Began restructuring the React frontend into smaller components.
- Extracted Pokémon result rendering into `PokemonCard`.
- Created `PokemonCard.css` and moved card-specific styling out of `App.css`.
- Extracted filter controls into `FilterPanel`.
- Kept filter state in `App` while passing values and change callbacks to
  `FilterPanel` through props.
- Moved generation, Legendary, Mythical, and BST controls into `FilterPanel`.
- Created `FilterPanel.css` and moved filter-specific styling out of
  `App.css`.
- Reviewed React props and parent/child component communication.
- Created a TypeScript `GenerateRequest` interface representing the FastAPI
  request contract.
- Replaced the anonymous generation request object with a typed
  `GenerateRequest`.
- Created `services/pokemonApi.ts`.
- Extracted HTTP communication and response parsing from `App.tsx` into
  `generatePokemon()`.
- Verified generation, filters, invalid requests, and network-error behavior
  continue to work after the refactor.
- Created a project roadmap for future feature planning.

### Current Frontend Structure

src/
├── components/
│   ├── FilterPanel.tsx
│   ├── FilterPanel.css
│   ├── PokemonCard.tsx
│   └── PokemonCard.css
├── services/
│   └── pokemonApi.ts
├── types/
│   ├── generateRequest.ts
│   └── pokemon.ts
├── App.tsx
├── App.css
├── index.css
└── main.tsx

### Next Steps

- Continue refining the component/API boundaries as needed.
- Begin deliberate Pokémon card/UI design work.
- Decide how Pokémon artwork should be represented.
- Select the next functional feature from `docs/roadmap.md`.