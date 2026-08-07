import random

from app.models.pokemon import Pokemon


def generate_pokemon(
    pokemon_catalog: list[Pokemon],
    count: int = 3,
) -> list[Pokemon]:
    """Select a specified number of unique Pokemon at random."""

    if count > len(pokemon_catalog):
        raise ValueError("Cannot generate more Pokemon than are available in the catalog.")

    return random.sample(pokemon_catalog, count)