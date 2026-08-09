import json

from urllib.request import Request, urlopen
from app.models.pokemon import Pokemon


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


def fetch_json(url: str) -> dict:
    """Fetch a JSON response from the provided URL."""

    request = Request(
        url,
        headers={
            "User-Agent": "pokemon-randomizer/0.1",
            "Accept": "application/json",
        },
    )

    print(f"Fetching: {url}")

    with urlopen(request, timeout=10) as response:
        return json.load(response)


def get_generation_number(generation_url: str) -> int:
    """Extract the numeric generation ID from a PokéAPI URL."""

    return int(
        generation_url.rstrip("/").split("/")[-1]
    )


def import_pokemon(pokedex_number: int) -> Pokemon:
    """Fetch and transform one Pokémon into our application's format."""

    species_data = fetch_json(
        f"{POKEAPI_BASE_URL}/pokemon-species/{pokedex_number}"
    )

    pokemon_data = fetch_json(
        f"{POKEAPI_BASE_URL}/pokemon/{pokedex_number}"
    )

    types = [
        type_entry["type"]["name"].title()
        for type_entry in pokemon_data["types"]
    ]

    return Pokemon(
        pokedex_number=species_data["id"],
        name=species_data["name"].title(),
        generation=get_generation_number(
            species_data["generation"]["url"]
        ),
        types=types,
        is_legendary=species_data["is_legendary"],
    )


if __name__ == "__main__":
    pokemon = import_pokemon(1)

    print(
        json.dumps(
            pokemon.model_dump(),
            indent=2,
        )
    )