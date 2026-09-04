from app.models.ability import Ability
from app.tools.pokeapi_client import POKEAPI_BASE_URL, fetch_json


def get_english_name(ability_data: dict) -> str:
    """Return the English display name for a Pokemon ability."""
    
    for name_entry in ability_data["names"]:
        if name_entry["language"]["name"] == "en":
            return name_entry["name"]
    
    raise ValueError("Pokemon ability does not contain an English name.")

def get_english_description(ability_data: dict) -> str:
    """Return the English display name for a Pokemon ability."""
    
    for effect_entry in ability_data["effect_entries"]:
        if effect_entry["language"]["name"] == "en":
            return effect_entry["short_effect"]
    
    raise ValueError("Pokemon ability does not contain an English description.")

def import_ability(ability_id: int) -> Ability:
    """Fetch and transform one Pokemon ability into our application's format."""
    
    ability_data = fetch_json(
        f"{POKEAPI_BASE_URL}/ability/{ability_id}"
    )
    
    return Ability(
        id=ability_data["id"],
        name=get_english_name(ability_data),
        description=get_english_description(ability_data),
    )