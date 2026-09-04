from pathlib import Path

import pytest

import app.tools.import_pokemon as importer
from app.tools.import_pokemon import get_resource_id
from app.models.pokemon import Pokemon
from app.services.pokemon_loader import load_pokemon


def test_get_resource_id_extracts_numeric_id() -> None:
    generation_url = "https://pokeapi.co/api/v2/generation/3/"

    result = get_resource_id(generation_url)

    assert result == 3


def test_import_pokemon_transforms_api_data(
    monkeypatch,
) -> None:
    species_response = {
        "id": 1,
        "name": "bulbasaur",
        "generation": {"url": "https://pokeapi.co/api/v2/generation/1/"},
        "is_legendary": False,
        "is_mythical": False,
        "names": [
            {
                "name": "Bulbasaur",
                "language": {"name": "en"},
            }
        ],
        "varieties": [
            {
                "is_default": True,
                "pokemon": {
                    "name": "bulbasaur",
                    "url": "https://pokeapi.co/api/v2/pokemon/1/",
                },
            }
        ],
    }

    pokemon_response = {
        "types": [
            {"type": {"name": "grass"}},
            {"type": {"name": "poison"}},
        ],
        "stats": [
            {
                "base_stat": 45,
                "stat": {"name": "hp"},
            },
            {
                "base_stat": 49,
                "stat": {"name": "attack"},
            },
            {
                "base_stat": 49,
                "stat": {"name": "defense"},
            },
            {
                "base_stat": 65,
                "stat": {"name": "special-attack"},
            },
            {
                "base_stat": 65,
                "stat": {"name": "special-defense"},
            },
            {
                "base_stat": 45,
                "stat": {"name": "speed"},
            },
        ],
    }

    def fake_fetch_json(url: str) -> dict:
        if "pokemon-species" in url:
            return species_response

        return pokemon_response

    monkeypatch.setattr(
        importer,
        "fetch_json",
        fake_fetch_json,
    )

    pokemon = importer.import_pokemon(1)

    assert isinstance(pokemon, Pokemon)
    assert pokemon.pokedex_number == 1
    assert pokemon.name == "Bulbasaur"
    assert pokemon.generation == 1
    assert pokemon.types == ["Grass", "Poison"]
    assert pokemon.is_legendary is False
    assert pokemon.is_mythical is False
    assert pokemon.hp == 45
    assert pokemon.attack == 49
    assert pokemon.defense == 49
    assert pokemon.special_attack == 65
    assert pokemon.special_defense == 65
    assert pokemon.speed == 45


def test_get_base_stats_maps_stats_by_name() -> None:
    pokemon_data = {
        "stats": [
            {
                "base_stat": 45,
                "stat": {"name": "hp"},
            },
            {
                "base_stat": 49,
                "stat": {"name": "attack"},
            },
        ]
    }

    result = importer.get_base_stats(pokemon_data)

    assert result == {
        "hp": 45,
        "attack": 49,
    }


def test_import_pokedex_imports_requested_pokemon(
    monkeypatch,
) -> None:
    imported_numbers = []

    def fake_import_pokemon(pokedex_number: int) -> Pokemon:
        imported_numbers.append(pokedex_number)

        return Pokemon(
            pokedex_number=pokedex_number,
            name=f"Pokemon {pokedex_number}",
            generation=1,
            types=["Normal"],
            hp=50,
            attack=50,
            defense=50,
            special_attack=50,
            special_defense=50,
            speed=50,
            is_legendary=False,
            is_mythical=False,
        )

    monkeypatch.setattr(
        importer,
        "import_pokemon",
        fake_import_pokemon,
    )

    result = importer.import_pokedex([1, 4, 7])

    assert imported_numbers == [1, 4, 7]
    assert len(result) == 3
    assert [pokemon.pokedex_number for pokemon in result] == [1, 4, 7]


def test_write_pokemon_json_can_be_loaded_back(
    tmp_path: Path,
) -> None:
    pokemon = [
        Pokemon(
            pokedex_number=151,
            name="Mew",
            generation=1,
            types=["Psychic"],
            hp=50,
            attack=50,
            defense=50,
            special_attack=50,
            special_defense=50,
            speed=50,
            is_legendary=False,
            is_mythical=True,
        ),
        Pokemon(
            pokedex_number=150,
            name="Mewtwo",
            generation=1,
            types=["Psychic"],
            hp=50,
            attack=50,
            defense=50,
            special_attack=50,
            special_defense=50,
            speed=50,
            is_legendary=True,
            is_mythical=False,
        ),
    ]

    output_file = tmp_path / "pokemon.json"

    importer.write_pokemon_json(
        pokemon,
        output_file,
    )

    loaded_pokemon = load_pokemon(output_file)

    assert loaded_pokemon == pokemon


def test_get_pokedex_numbers_follows_pagination(
    monkeypatch,
) -> None:
    first_page = {
        "results": [
            {
                "name": "bulbasaur",
                "url": "https://pokeapi.co/api/v2/pokemon-species/1/",
            },
            {
                "name": "ivysaur",
                "url": "https://pokeapi.co/api/v2/pokemon-species/2/",
            },
        ],
        "next": "https://example.com/page-2",
    }

    second_page = {
        "results": [
            {
                "name": "venusaur",
                "url": "https://pokeapi.co/api/v2/pokemon-species/3/",
            },
        ],
        "next": None,
    }

    def fake_fetch_json(url: str) -> dict:
        if url == importer.POKEMON_SPECIES_LIST_URL:
            return first_page

        return second_page

    monkeypatch.setattr(
        importer,
        "fetch_json",
        fake_fetch_json,
    )

    result = importer.get_pokedex_numbers()

    assert result == [1, 2, 3]


def test_get_english_name_returns_english_display_name() -> None:
    species_data = {
        "names": [
            {
                "name": "Pantimos",
                "language": {"name": "de"},
            },
            {
                "name": "Mr. Mime",
                "language": {"name": "en"},
            },
        ]
    }

    result = importer.get_english_name(species_data)

    assert result == "Mr. Mime"


def test_validate_pokedex_accepts_complete_catalog() -> None:
    pokemon = [
        Pokemon(
            pokedex_number=1,
            name="Pokemon 1",
            generation=1,
            types=["Normal"],
            hp=50,
            attack=50,
            defense=50,
            special_attack=50,
            special_defense=50,
            speed=50,
            is_legendary=False,
            is_mythical=False,
        ),
        Pokemon(
            pokedex_number=2,
            name="Pokemon 2",
            generation=1,
            types=["Normal"],
            hp=50,
            attack=50,
            defense=50,
            special_attack=50,
            special_defense=50,
            speed=50,
            is_legendary=False,
            is_mythical=False,
        ),
    ]

    importer.validate_pokedex(
        pokemon,
        [1, 2],
    )


def test_validate_pokedex_rejects_missing_pokemon() -> None:
    pokemon = [
        Pokemon(
            pokedex_number=1,
            name="Pokemon 1",
            generation=1,
            types=["Normal"],
            hp=50,
            attack=50,
            defense=50,
            special_attack=50,
            special_defense=50,
            speed=50,
            is_legendary=False,
            is_mythical=False,
        ),
    ]

    with pytest.raises(
        ValueError,
        match="Pokedex numbers do not match",
    ):
        importer.validate_pokedex(
            pokemon,
            [1, 2],
        )


def test_load_pokemon_rejects_non_array_json(
    tmp_path: Path,
) -> None:
    data_file = tmp_path / "pokemon.json"

    data_file.write_text(
        '{"name": "Bulbasaur"}',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Pokemon data file must contain a JSON array",
    ):
        load_pokemon(data_file)
