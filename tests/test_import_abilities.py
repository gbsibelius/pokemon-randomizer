import pytest

import app.tools.import_abilities as importer
from app.models.ability import Ability


def make_ability(
    ability_id: int,
    name: str = "Stench",
    description: str = "May cause the target to flinch.",
) -> Ability:
    return Ability(
        id=ability_id,
        name=name,
        description=description,
    )

def test_import_ability_transforms_api_data() -> None:
    ability_response = {
        "id": 1,
        "names": [
            {
                "name": "Stench",
                "language": {"name": "en"},
            }
        ],
        "effect_entries": [
            {
                "short_effect": "May cause the target to flinch.",
                "language": {"name": "en"},
            }
        ],
    }

    ability = importer.import_ability(ability_response)

    assert isinstance(ability, Ability)
    assert ability.id == 1
    assert ability.name == "Stench"
    assert ability.description == "May cause the target to flinch."

def test_import_abilities_excludes_non_main_series(
    monkeypatch,
) -> None:
    ability_resources = [
        {
            "name": "stench",
            "url": "https://pokeapi.co/api/v2/ability/1/",
        },
        {
            "name": "side-game-ability",
            "url": "https://pokeapi.co/api/v2/ability/2/",
        },
    ]

    main_series_response = {
        "id": 1,
        "is_main_series": True,
        "names": [
            {
                "name": "Stench",
                "language": {"name": "en"},
            }
        ],
        "effect_entries": [
            {
                "short_effect": "May cause the target to flinch.",
                "language": {"name": "en"},
            }
        ],
    }

    non_main_series_response = {
        "id": 2,
        "is_main_series": False,
        "names": [
            {
                "name": "Side Game Ability",
                "language": {"name": "en"},
            }
        ],
        "effect_entries": [
            {
                "short_effect": "Not relevant to the main-series pool.",
                "language": {"name": "en"},
            }
        ],
    }

    def fake_fetch_json(url: str) -> dict:
        if url.endswith("/1/"):
            return main_series_response

        if url.endswith("/2/"):
            return non_main_series_response

        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(
        importer,
        "fetch_json",
        fake_fetch_json,
    )

    abilities = importer.import_abilities(ability_resources)

    assert len(abilities) == 1
    assert abilities[0].id == 1
    assert abilities[0].name == "Stench"

def test_validate_abilities_accepts_valid_dataset() -> None:
    abilities = [
        make_ability(1),
        make_ability(2, name="Drizzle"),
    ]

    importer.validate_abilities(abilities)

def test_validate_abilities_rejects_duplicate_ids() -> None:
    abilities = [
        make_ability(1),
        make_ability(1, name="Drizzle"),
    ]

    with pytest.raises(ValueError):
        importer.validate_abilities(abilities)

def test_validate_abilities_rejects_blank_description() -> None:
    abilities = [
        make_ability(
            1,
            description="   ",
        ),
    ]

    with pytest.raises(ValueError):
        importer.validate_abilities(abilities)

def test_validate_abilities_rejects_blank_name() -> None:
    abilities = [
        make_ability(
            1,
            name="   ",
        ),
    ]

    with pytest.raises(ValueError):
        importer.validate_abilities(abilities)

def test_validate_abilities_rejects_empty_dataset() -> None:
    with pytest.raises(ValueError):
        importer.validate_abilities([])
