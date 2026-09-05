import json
from pathlib import Path

from app.models.ability import Ability
from app.tools.pokeapi_client import POKEAPI_BASE_URL, fetch_json


ABILITY_LIST_URL = f"{POKEAPI_BASE_URL}/ability?limit=100"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def get_english_name(ability_data: dict) -> str:
    """Return the English display name for a Pokemon ability."""
    
    for name_entry in ability_data["names"]:
        if name_entry["language"]["name"] == "en":
            return name_entry["name"]
    
    raise ValueError("Pokemon ability does not contain an English name.")

def get_english_description(ability_data: dict) -> str:
    """Return the English short description for a Pokemon ability."""
    
    for effect_entry in ability_data["effect_entries"]:
        if effect_entry["language"]["name"] == "en":
            return effect_entry["short_effect"]
    
    raise ValueError("Pokemon ability does not contain an English description.")

def get_ability_resources() -> list[dict]:
    """Return all ability resources available from PokeAPI."""

    ability_resources = []
    next_url = ABILITY_LIST_URL

    while next_url is not None:
        page_data = fetch_json(next_url)

        ability_resources.extend(page_data["results"])
        next_url = page_data["next"]

    return ability_resources

def get_non_main_series_abilities() -> list[tuple[int, str]]:
    """Return IDs and names for abilities not marked as main-series."""

    non_main_series = []

    for resource in get_ability_resources():
        ability_data = fetch_json(resource["url"])

        if not ability_data["is_main_series"]:
            non_main_series.append(
                (
                    ability_data["id"],
                    ability_data["name"],
                )
            )

    return non_main_series

def import_ability(ability_data: dict) -> Ability:
    """Transform one Pokemon ability into our application's format."""

    return Ability(
        id=ability_data["id"],
        name=get_english_name(ability_data),
        description=get_english_description(ability_data),
    )

def import_abilities(ability_resources: list[dict]) -> list[Ability]:
    imported_abilities = []

    total = len(ability_resources)

    for index, resource in enumerate(
        ability_resources,
        start=1,
    ):
        print(f"Importing ability {index}/{total}: " f"{resource['name']}")

        ability_data = fetch_json(resource["url"])

        if not ability_data["is_main_series"]:
            continue

        ability = import_ability(ability_data)
        imported_abilities.append(ability)

    return imported_abilities

def validate_abilities(abilities: list[Ability]) -> None:
    """Validate that the imported ability dataset is internally consistent."""

    if not abilities:
        raise ValueError("Abilities list is empty.")

    ability_ids = [ability.id for ability in abilities]

    if len(ability_ids) != len(set(ability_ids)):
        raise ValueError("Abilities list contains a duplicate.")

    for ability in abilities:
        if not ability.name.strip():
            raise ValueError(f"Ability #{ability.id} has an empty name.")

        if not ability.description.strip():
            raise ValueError(f"Ability #{ability.id} has an empty description.")

def write_abilities_json(
    abilities: list[Ability],
    file_path: Path,
) -> None:
    """Write Ability records to a JSON file."""

    ability_data = [ability.model_dump() for ability in abilities]

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            ability_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")

if __name__ == "__main__":
    ability_resources = get_ability_resources()

    print(f"Discovered {len(ability_resources)} ability resources.")

    abilities = import_abilities(ability_resources)

    print(f"Imported {len(abilities)} main-series abilities.")

    validate_abilities(abilities)

    preview_file = REPOSITORY_ROOT / "data" / "abilities_preview.json"

    write_abilities_json(
        abilities,
        preview_file,
    )

    print(f"Wrote {len(abilities)} abilities to " f"{preview_file}")
