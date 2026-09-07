import json
from pathlib import Path

from app.models.ability import Ability


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

ABILITY_DATA_FILE = REPOSITORY_ROOT / "data" / "abilities_preview.json"

ABILITY_OVERRIDES_FILE = REPOSITORY_ROOT / "data" / "ability_overrides.json"


def apply_ability_overrides(
    abilities: list[Ability],
    overrides: dict,
) -> list[Ability]:
    updated_abilities = []

    allowed_fields = {"name", "description"}

    for ability in abilities:
        override = overrides.get(str(ability.id))

        if override is None:
            updated_abilities.append(ability)
            continue

        unexpected_fields = set(override) - allowed_fields

        if unexpected_fields:
            raise ValueError(
                "Ability override contains unsupported fields: " f"{unexpected_fields}"
            )

        updated_data = ability.model_dump()
        updated_data.update(override)

        updated_ability = Ability.model_validate(updated_data)

        updated_abilities.append(updated_ability)

    return updated_abilities

def load_abilities(
    abilities_path: Path | None = None,
    overrides_path: Path | None = None,
) -> list[Ability]:
    
    ability_file = abilities_path or ABILITY_DATA_FILE
    override_file = overrides_path or ABILITY_OVERRIDES_FILE

    with ability_file.open("r", encoding="utf-8") as file:
        raw_abilities = json.load(file)

    with override_file.open("r", encoding="utf-8") as file:
        overrides = json.load(file)

    if not isinstance(raw_abilities, list):
        raise ValueError(
            "Ability data file must contain a JSON array."
        )

    if not isinstance(overrides, dict):
        raise ValueError(
            "Ability overrides file must contain a JSON object."
    )

    abilities = [
        Ability.model_validate(item)
        for item in raw_abilities
    ]

    return apply_ability_overrides(
        abilities,
        overrides,
    )
