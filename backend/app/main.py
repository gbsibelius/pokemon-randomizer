from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.models.pokemon import Pokemon
from app.models.generated_pokemon import GeneratedPokemon
from app.models.generate_request import GenerateRequest
from app.services.pokemon_loader import load_pokemon
from app.services.randomizer_service import generate_pokemon, create_generated_pokemon

app = FastAPI(title="Pokemon Randomizer API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

pokemon_catalog: list[Pokemon] = load_pokemon()

@app.get("/")
def read_root() -> dict[str, str]:
    """Return a basic status message for the API."""

    return {"message": "Pokemon Randomizer API is running"}

@app.get("/pokemon", response_model=list[Pokemon])
def get_all_pokemon() -> list[Pokemon]:
    """Return every Pokemon available to the randomizer."""

    return pokemon_catalog

@app.post("/generate", response_model=list[GeneratedPokemon])
def generate_random_pokemon(
    request: GenerateRequest,
) -> list[GeneratedPokemon]:
    """Generate three unique random Pokemon according to supplied rules."""

    try:
        selected_pokemon = generate_pokemon(
            pokemon_catalog,
            count=request.count,
            generations=request.generations,
            exclude_legendaries=request.exclude_legendaries,
            exclude_mythicals=request.exclude_mythicals,
            min_bst=request.min_bst,
            max_bst=request.max_bst,
            exclude_pokedex_numbers=request.exclude_pokedex_numbers,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    generated_pokemon = [
        create_generated_pokemon(
            pokemon,
            shiny_chance=request.shiny_chance,
        )
        for pokemon in selected_pokemon
    ]

    return generated_pokemon