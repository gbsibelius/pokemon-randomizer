import random

from app.models.pokemon import Pokemon


def generate_pokemon(
    pokemon_catalog: list[Pokemon],
    count: int = 3,
    generations: list[int] | None = None,
    exclude_legendaries: bool = False,
) -> list[Pokemon]:
    """Select a specified number of unique Pokemon at random."""

    eligible_pokemon = pokemon_catalog

    if generations is not None:
        eligible_pokemon = [
            pokemon
            for pokemon in eligible_pokemon
            if pokemon.generation in generations
        ]

    if exclude_legendaries:
        eligible_pokemon = [
            pokemon
            for pokemon in eligible_pokemon
            if not pokemon.is_legendary
        ]

    if count > len(eligible_pokemon):
        raise ValueError("Cannot generate the requested number of Pokemon with the supplied filters.")

    return random.sample(eligible_pokemon, count)