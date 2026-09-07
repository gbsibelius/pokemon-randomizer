import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

ABILITIES_FILE = REPOSITORY_ROOT / "data" / "abilities_preview.json"

ABILITY_TIERS_FILE = REPOSITORY_ROOT / "data" / "ability_tiers.json"


def generate_ability_tiers() -> None:
    """Create an unassigned ability-tier scaffold."""

    if ABILITY_TIERS_FILE.exists():
        raise FileExistsError("ability_tiers.json already exists.")

    with ABILITIES_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        abilities = json.load(file)

    tier_data = {
        str(ability["id"]): {
            "name": ability["name"],
            "tier": "unassigned",
        }
        for ability in abilities
    }

    with ABILITY_TIERS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            tier_data,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")


if __name__ == "__main__":
    generate_ability_tiers()
