import pytest
import json
from pathlib import Path

from app.models.ability import Ability
from app.services.ability_loader import apply_ability_overrides, load_abilities


def make_ability() -> Ability:
    return Ability(
        id=1,
        name="Stench",
        description="Original description.",
    )


def test_apply_ability_overrides_keeps_ability_without_override() -> None:
    ability = make_ability()

    result = apply_ability_overrides(
        [ability],
        {},
    )

    assert len(result) == 1
    assert result[0] == ability


def test_apply_ability_overrides_replaces_description() -> None:
    ability = make_ability()

    overrides = {
        "1": {
            "description": "Updated description.",
        }
    }

    result = apply_ability_overrides(
        [ability],
        overrides,
    )

    assert result[0].id == 1
    assert result[0].name == "Stench"
    assert result[0].description == "Updated description."


def test_apply_ability_overrides_replaces_name() -> None:
    ability = make_ability()

    overrides = {
        "1": {
            "name": "Updated Name",
        }
    }

    result = apply_ability_overrides(
        [ability],
        overrides,
    )

    assert result[0].id == 1
    assert result[0].name == "Updated Name"
    assert result[0].description == "Original description."

def test_apply_ability_overrides_rejects_unsupported_field() -> None:
    ability = make_ability()

    overrides = {
        "1": {
            "id": 999,
        }
    }

    with pytest.raises(
        ValueError,
        match="unsupported fields",
    ):
        apply_ability_overrides(
            [ability],
            overrides,
        )

def test_load_abilities_applies_overrides(
    tmp_path: Path,
) -> None:
    abilities_file = tmp_path / "abilities.json"
    overrides_file = tmp_path / "ability_overrides.json"

    abilities_data = [
        {
            "id": 1,
            "name": "Stench",
            "description": "Original description.",
        },
        {
            "id": 2,
            "name": "Drizzle",
            "description": "Original Drizzle description.",
        },
    ]

    overrides_data = {
        "2": {
            "description": "Updated Drizzle description.",
        }
    }

    abilities_file.write_text(
        json.dumps(abilities_data),
        encoding="utf-8",
    )

    overrides_file.write_text(
        json.dumps(overrides_data),
        encoding="utf-8",
    )

    result = load_abilities(
        abilities_file,
        overrides_file,
    )

    assert len(result) == 2

    assert result[0].name == "Stench"
    assert result[0].description == "Original description."

    assert result[1].name == "Drizzle"
    assert result[1].description == "Updated Drizzle description."

def test_load_abilities_rejects_non_array_ability_data(
    tmp_path: Path,
) -> None:
    abilities_file = tmp_path / "abilities.json"
    overrides_file = tmp_path / "ability_overrides.json"

    abilities_file.write_text(
        '{"id": 1, "name": "Stench"}',
        encoding="utf-8",
    )

    overrides_file.write_text(
        "{}",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Ability data file must contain a JSON array",
    ):
        load_abilities(
            abilities_file,
            overrides_file,
        )

def test_load_abilities_rejects_non_object_overrides(
    tmp_path: Path,
) -> None:
    abilities_file = tmp_path / "abilities.json"
    overrides_file = tmp_path / "ability_overrides.json"

    abilities_data = [
        {
            "id": 1,
            "name": "Stench",
            "description": "Original description.",
        }
    ]

    abilities_file.write_text(
        json.dumps(abilities_data),
        encoding="utf-8",
    )

    overrides_file.write_text(
        "[]",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Ability overrides file must contain a JSON object",
    ):
        load_abilities(
            abilities_file,
            overrides_file,
        )

def test_load_abilities_loads_real_dataset() -> None:
    abilities = load_abilities()

    assert len(abilities) == 314
