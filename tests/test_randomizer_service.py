import pytest

from app.models.pokemon import Pokemon
from app.services import randomizer_service
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
            hp=45,
            attack=49,
            defense=49,
            special_attack=65,
            special_defense=65,
            speed=45,
            is_legendary=False,
            is_mythical=False,
        ),
        Pokemon(
            pokedex_number=25,
            name="Pikachu",
            generation=1,
            types=["Electric"],
            hp=35,
            attack=55,
            defense=40,
            special_attack=50,
            special_defense=50,
            speed=90,
            is_legendary=False,
            is_mythical=False,
        ),
        Pokemon(
            pokedex_number=150,
            name="Mewtwo",
            generation=1,
            types=["Psychic"],
            hp=106,
            attack=110,
            defense=90,
            special_attack=154,
            special_defense=90,
            speed=130,
            is_legendary=True,
            is_mythical=False,
        ),
        Pokemon(
            pokedex_number=151,
            name="Mew",
            generation=1,
            types=["Psychic"],
            hp=100,
            attack=100,
            defense=100,
            special_attack=100,
            special_defense=100,
            speed=100,
            is_legendary=False,
            is_mythical=True,
        ),
        Pokemon(
            pokedex_number=152,
            name="Chikorita",
            generation=2,
            types=["Grass"],
            hp=45,
            attack=49,
            defense=65,
            special_attack=49,
            special_defense=65,
            speed=45,
            is_legendary=False,
            is_mythical=False,
        ),
        Pokemon(
            pokedex_number=155,
            name="Cyndaquil",
            generation=2,
            types=["Fire"],
            hp=39,
            attack=52,
            defense=43,
            special_attack=60,
            special_defense=50,
            speed=65,
            is_legendary=False,
            is_mythical=False,
        ),
        Pokemon(
            pokedex_number=158,
            name="Totodile",
            generation=2,
            types=["Water"],
            hp=50,
            attack=65,
            defense=64,
            special_attack=44,
            special_defense=48,
            speed=43,
            is_legendary=False,
            is_mythical=False,
        ),
    ]

def test_generate_pokemon_returns_three_by_default(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(sample_catalog)

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

def test_excluded_pokedex_numbers_are_excluded(
    sample_catalog: list[Pokemon],
) -> None:
    excluded_numbers = [1, 25, 150]
    
    result = generate_pokemon(
        sample_catalog,
        count=3,
        exclude_pokedex_numbers=excluded_numbers,
    )

    assert all(
        pokemon.pokedex_number not in excluded_numbers
        for pokemon in result
    )

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

def test_exclude_mythicals_removes_mythical_pokemon(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(
        sample_catalog,
        count=3,
        generations=[1],
        exclude_mythicals=True,
    )

    assert all(
        not pokemon.is_mythical
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

def test_generate_pokemon_raises_value_error_when_reroll_pool_is_too_small(
    sample_catalog: list[Pokemon],
) -> None:
    with pytest.raises(
        ValueError,
        match="Cannot generate the requested number of Pokemon with the supplied filters.",
    ):
        generate_pokemon(
            sample_catalog,
            count=3,
            generations=[2],
            exclude_pokedex_numbers=[152]
        )

def test_pokemon_bst_sums_base_stats() -> None:
    pokemon = Pokemon(
        pokedex_number=1,
        name="Bulbasaur",
        generation=1,
        types=["Grass", "Poison"],
        hp=45,
        attack=49,
        defense=49,
        special_attack=65,
        special_defense=65,
        speed=45,
        is_legendary=False,
        is_mythical=False,
    )

    assert pokemon.bst == 318

def test_min_bst_filter_removes_lower_bst_pokemon(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(
        sample_catalog,
        count=2,
        min_bst=500,
    )

    assert all(
        pokemon.bst >= 500
        for pokemon in result
    )

def test_max_bst_filter_removes_higher_bst_pokemon(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(
        sample_catalog,
        count=2,
        max_bst=315,
    )

    assert all(
        pokemon.bst <= 315
        for pokemon in result
    )

def test_bst_range_only_returns_pokemon_within_range(
    sample_catalog: list[Pokemon],
) -> None:
    result = generate_pokemon(
        sample_catalog,
        count=3,
        min_bst=315,
        max_bst=320,
    )

    assert all(
        315 <= pokemon.bst <= 320
        for pokemon in result
    )

def test_create_generated_pokemon_is_shiny_when_roll_is_within_chance(
    sample_catalog: list[Pokemon],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pokemon = sample_catalog[0]

    monkeypatch.setattr(
        randomizer_service.random,
        "randint",
        lambda _start, _end: 5,
    )

    result = randomizer_service.create_generated_pokemon(
        pokemon,
        shiny_chance=5,
    )

    assert result.pokemon == pokemon
    assert result.is_shiny is True

def test_create_generated_pokemon_is_not_shiny_when_roll_exceeds_chance(
    sample_catalog: list[Pokemon],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pokemon = sample_catalog[0]

    monkeypatch.setattr(
        randomizer_service.random,
        "randint",
        lambda _start, _end: 6,
    )

    result = randomizer_service.create_generated_pokemon(
        pokemon,
        shiny_chance=5,
    )

    assert result.pokemon == pokemon
    assert result.is_shiny is False

def test_create_generated_pokemon_rejects_invalid_shiny_chance(
    sample_catalog: list[Pokemon],
) -> None:
    pokemon = sample_catalog[0]

    with pytest.raises(
        ValueError,
        match="shiny_chance must be between 0 and 100.",
    ):
        randomizer_service.create_generated_pokemon(
            pokemon,
            shiny_chance=101,
        )