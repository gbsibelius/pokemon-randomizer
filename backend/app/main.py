from fastapi import FastAPI

from app.models.pokemon import Pokemon
from app.services.pokemon_loader import load_pokemon

app = FastAPI(title="Pokemon Randomizer API")

pokemon_catalog: list[Pokemon] = load_pokemon()

@app.get("/")
def read_root() -> dict[str, str]:
    """Return a basic status message for the API."""

    return {"message": "Pokemon Randomizer API is running"}

@app.get("/pokemon", response_model=list[Pokemon])
def get_all_pokemon() -> list[Pokemon]:
    """Return every Pokemon available to the randomizer."""

    return pokemon_catalog