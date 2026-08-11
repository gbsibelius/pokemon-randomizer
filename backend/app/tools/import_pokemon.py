import json
import time

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from app.models.pokemon import Pokemon
from pathlib import Path


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
POKEMON_SPECIES_LIST_URL = (
    f"{POKEAPI_BASE_URL}/pokemon-species?limit=100"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def fetch_json(url: str) -> dict:
    """Fetch a JSON response from the provided URL."""

    request = Request(
        url,
        headers={
            "User-Agent": "pokemon-randomizer/0.1",
            "Accept": "application/json",
        },
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(
                request,
                timeout=10,
            ) as response:
                return json.load(response)

        except HTTPError as error:
            if error.code not in {
                429,
                500,
                502,
                503,
                504,
            }:
                raise

            if attempt == MAX_RETRIES:
                raise

            print(
                f"HTTP {error.code}. "
                f"Retrying ({attempt}/{MAX_RETRIES})..."
            )

        except (URLError, TimeoutError) as error:
            if attempt == MAX_RETRIES:
                raise

            print(
                f"Network error: {error}. "
                f"Retrying ({attempt}/{MAX_RETRIES})..."
            )

        time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError("Failed to fetch PokéAPI data.")

def get_default_variety_url(species_data: dict) -> str:
    """Return the PokéAPI URL for a species' default Pokémon variety."""

    for variety in species_data["varieties"]:
        if variety["is_default"]:
            return variety["pokemon"]["url"]

    raise ValueError("Pokemon species does not contain a default variety.")

def get_english_name(species_data: dict) -> str:
    """Return the English display name for a Pokémon species."""

    for name_entry in species_data["names"]:
        if name_entry["language"]["name"] == "en":
            return name_entry["name"]

    raise ValueError("Pokemon species does not contain an English name.")

def get_resource_id(resource_url: str) -> int:
    """Extract the numeric resource ID from a PokéAPI URL."""

    return int(
        resource_url.rstrip("/").split("/")[-1]
    )

def get_base_stats(pokemon_data: dict) -> dict[str, int]:
    """Return base stats keyed by PokéAPI stat name."""

    return {
        stat_entry["stat"]["name"]: stat_entry["base_stat"]
        for stat_entry in pokemon_data["stats"]
    }

def get_pokedex_numbers() -> list[int]:
    """Retrieve all Pokémon species IDs available from PokéAPI."""

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
    """Validate that an imported Pokédex is complete and internally consistent."""

    actual_pokedex_numbers = [
        entry.pokedex_number
        for entry in pokemon
    ]

    if actual_pokedex_numbers != expected_pokedex_numbers:
        raise ValueError(
            "Imported Pokédex numbers do not match "
            "the discovered Pokédex numbers."
        )

    for entry in pokemon:
        if not entry.types:
            raise ValueError(
                f"{entry.name} does not have any Pokémon types."
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
    """Fetch and transform one Pokémon into our application's format."""

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
        name=species_data["name"].title(),
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

def import_pokedex(pokedex_numbers:  list[int]) -> list[Pokemon]:
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
        f"Discovered {len(pokedex_numbers)} Pokémon species."
    )

    pokemon = import_pokedex(pokedex_numbers)

    validate_pokedex(
        pokemon,
        pokedex_numbers,
    )

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
        f"Wrote {len(pokemon)} Pokémon to "
        f"{preview_file}"
    )
