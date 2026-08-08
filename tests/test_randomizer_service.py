import pytest

from app.models.pokemon import Pokemon
from app.services.randomizer_service import generate_pokemon


@pytest.fixture
def sample_catalog() -> list[Pokemon]:
    """Provide a small predictable Pokemon catalog for randomizer tests."""

    return [
        Pokemon(
            pokedex_number=1,
            name="Bulbasaur",
            generation=1,
            types=["Grass", "Poison"],
            is_legendary=False,
        ),
        Pokemon(
            pokedex_number=25,
            name="Pikachu",
            generation=1,
            types=["Electric"],
            is_legendary=False,
        ),
        Pokemon(
            pokedex_number=150,
            name="Mewtwo",
            generation=1,
            types=["Psychic"],
            is_legendary=True,
        ),
        Pokemon(
            pokedex_number=152,
            name="Chikorita",
            generation=2,
            types=["Grass"],
            is_legendary=False,
        ),
        Pokemon(
            pokedex_number=155,
            name="Cyndaquil",
            generation=2,
            types=["Fire"],
            is_legendary=False,
        ),
        Pokemon(
            pokedex_number=158,
            name="Totodile",
            generation=2,
            types=["Water"],
            is_legendary=False,
        ),
    ]

def test_generate_pokemon_returns_three_by_default(
    sample_catalog: list[Pokemon],
) -> None:
    catalog = sample_catalog

    result = generate_pokemon(catalog)

    assert len(result) == 3

def test_generate_pokemon_returns_unique_results(
        sample_catalog: list[Pokemon]
) -> None:
    result = generate_pokemon(sample_catalog)

    pokedex_numbers = [
        pokemon.pokedex_number
        for pokemon in result
    ]

    assert len(pokedex_numbers) == len(set(pokedex_numbers))

def test_generation_filter_only_returns_requested_generation(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(
        sample_catalog,
        count=3,
        generations=[2],
    )

    assert all(
        pokemon.generation == 2
        for pokemon in result
    )

def test_exclude_legendaries_removes_legendary_pokemon(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(
        sample_catalog,
        count=2,
        generations=[1],
        exclude_legendaries=True,
    )

    assert all(
        not pokemon.is_legendary
        for pokemon in result
    )

def test_generate_pokemon_raises_value_error_when_pool_is_too_small(
    sample_catalog: list[Pokemon],
) -> None:
    with pytest.raises(
        ValueError,
        match="Cannot generate the requested number of Pokemon with the supplied filters.",
    ):
        generate_pokemon(
            sample_catalog,
            count=4,
            generations=[2],
        )