import json
from pathlib import Path

from app.models.pokemon import Pokemon
from app.tools.pokeapi_client import POKEAPI_BASE_URL, fetch_json

POKEMON_SPECIES_LIST_URL = (
    f"{POKEAPI_BASE_URL}/pokemon-species?limit=100"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def get_default_variety_url(species_data: dict) -> str:
    """Return the PokeAPI URL for a species' default Pokemon variety."""

    for variety in species_data["varieties"]:
        if variety["is_default"]:
            return variety["pokemon"]["url"]

    raise ValueError("Pokemon species does not contain a default variety.")

def get_english_name(species_data: dict) -> str:
    """Return the English display name for a Pokemon species."""

    for name_entry in species_data["names"]:
        if name_entry["language"]["name"] == "en":
            return name_entry["name"]

    raise ValueError("Pokemon species does not contain an English name.")

def get_resource_id(resource_url: str) -> int:
    """Extract the numeric resource ID from a PokeAPI URL."""

    return int(
        resource_url.rstrip("/").split("/")[-1]
    )

def get_base_stats(pokemon_data: dict) -> dict[str, int]:
    """Return base stats keyed by PokeAPI stat name."""

    return {
        stat_entry["stat"]["name"]: stat_entry["base_stat"]
        for stat_entry in pokemon_data["stats"]
    }

def get_pokedex_numbers() -> list[int]:
    """Retrieve all Pokemon species IDs available from PokeAPI."""

    pokedex_numbers = []
    next_url = POKEMON_SPECIES_LIST_URL

    while next_url is not None:
        page_data = fetch_json(next_url)

        pokedex_numbers.extend(
            get_resource_id(entry["url"])
            for entry in page_data["results"]
        )

        next_url = page_data["next"]

    return pokedex_numbers

def validate_pokedex(
    pokemon: list[Pokemon],
    expected_pokedex_numbers: list[int],
) -> None:
    """Validate that an imported Pokedex is complete and internally consistent."""

    actual_pokedex_numbers = [
        entry.pokedex_number
        for entry in pokemon
    ]

    if actual_pokedex_numbers != expected_pokedex_numbers:
        raise ValueError(
            "Imported Pokedex numbers do not match "
            "the discovered Pokedex numbers."
        )

    for entry in pokemon:
        if not entry.types:
            raise ValueError(
                f"{entry.name} does not have any Pokemon types."
            )

        stats = [
            entry.hp,
            entry.attack,
            entry.defense,
            entry.special_attack,
            entry.special_defense,
            entry.speed,
        ]

        if any(stat <= 0 for stat in stats):
            raise ValueError(
                f"{entry.name} contains an invalid base stat."
            )

def import_pokemon(pokedex_number: int) -> Pokemon:
    """Fetch and transform one Pokemon into our application's format."""

    species_data = fetch_json(
        f"{POKEAPI_BASE_URL}/pokemon-species/{pokedex_number}"
    )

    default_variety_url = get_default_variety_url(species_data)
    pokemon_data = fetch_json(default_variety_url)
    base_stats = get_base_stats(pokemon_data)

    types = [
        type_entry["type"]["name"].title()
        for type_entry in pokemon_data["types"]
    ]

    return Pokemon(
        pokedex_number=species_data["id"],
        name=get_english_name(species_data),
        generation=get_resource_id(
            species_data["generation"]["url"]
        ),
        types=types,

        hp=base_stats["hp"],
        attack=base_stats["attack"],
        defense=base_stats["defense"],
        special_attack=base_stats["special-attack"],
        special_defense=base_stats["special-defense"],
        speed=base_stats["speed"],

        is_legendary=species_data["is_legendary"],
        is_mythical=species_data["is_mythical"],
    )

def import_pokedex(pokedex_numbers: list[int]) -> list[Pokemon]:
    """Import multiple Pokemon by National Pokedex number."""

    imported_pokemon = []
    total = len(pokedex_numbers)

    for index, pokedex_number in enumerate(
        pokedex_numbers,
        start=1,
    ):
        print(
            f"Importing {index}/{total} "
            f"(Pokédex #{pokedex_number})"
        )

        pokemon = import_pokemon(pokedex_number)
        imported_pokemon.append(pokemon)

    return imported_pokemon

def write_pokemon_json(
    pokemon: list[Pokemon],
    file_path: Path,
) -> None:
    """Write Pokemon records to a JSON file."""

    pokemon_data = [
        entry.model_dump()
        for entry in pokemon
    ]

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(
            pokemon_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")

if __name__ == "__main__":
    pokedex_numbers = get_pokedex_numbers()

    print(
        f"Discovered {len(pokedex_numbers)} Pokemon species."
    )

    pokemon = import_pokedex(pokedex_numbers)

    validate_pokedex(
        pokemon,
        pokedex_numbers,
    )

    # Write imports to a preview file for verifications before replacing pokemon.json
    preview_file = (
        REPOSITORY_ROOT
        / "data"
        / "pokemon_preview.json"
    )

    write_pokemon_json(
        pokemon,
        preview_file,
    )

    print(
        f"Wrote {len(pokemon)} Pokemon to "
        f"{preview_file}"
    )
