import random

from app.models.pokemon import Pokemon
from app.models.generated_pokemon import GeneratedPokemon

DEFAULT_SHINY_CHANCE = 1


def generate_pokemon(
    pokemon_catalog: list[Pokemon],
    count: int = 3,
    generations: list[int] | None = None,
    exclude_legendaries: bool = False,
    exclude_mythicals: bool = False,
    exclude_pokedex_numbers: list[int] | None = None,
    min_bst: int | None = None,
    max_bst: int | None = None,
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

    if exclude_mythicals:
        eligible_pokemon = [
            pokemon
            for pokemon in eligible_pokemon
            if not pokemon.is_mythical
        ]

    if exclude_pokedex_numbers is not None:
        eligible_pokemon = [
            pokemon
            for pokemon in eligible_pokemon
            if pokemon.pokedex_number not in exclude_pokedex_numbers
        ]

    if min_bst is not None:
        eligible_pokemon = [
            pokemon
            for pokemon in eligible_pokemon
            if pokemon.bst >= min_bst
        ]

    if max_bst is not None:
        eligible_pokemon = [
            pokemon
            for pokemon in eligible_pokemon
            if pokemon.bst <= max_bst
        ]

    if count > len(eligible_pokemon):
        raise ValueError("Cannot generate the requested number of Pokemon with the supplied filters.")

    return random.sample(eligible_pokemon, count)

def create_generated_pokemon(
    pokemon: Pokemon,
    shiny_chance: int = DEFAULT_SHINY_CHANCE,
) -> GeneratedPokemon:
    """Create a generated Pokemon result with a randomized shiny status."""
    if not 0 <= shiny_chance <= 100:
        raise ValueError("shiny_chance must be between 0 and 100.")
    
    roll = random.randint(1, 100)

    return GeneratedPokemon(
        pokemon=pokemon,
        is_shiny=roll <= shiny_chance,
    )