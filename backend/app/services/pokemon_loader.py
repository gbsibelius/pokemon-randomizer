import json
from pathlib import Path

from app.models.pokemon import Pokemon

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
POKEMON_DATA_FILE = REPOSITORY_ROOT / "data" / "pokemon.json"

def load_pokemon(file_path: Path | None = None) -> list[Pokemon]:
    """Load and validate Pokemon records from a JSON file."""

    path = file_path or POKEMON_DATA_FILE

    with path.open("r", encoding="utf-8") as file:
        raw_pokemon = json.load(file)

    if not isinstance(raw_pokemon, list):
        raise ValueError("Pokemon data file must contain a JSON array.")

    return [Pokemon.model_validate(item) for item in raw_pokemon]