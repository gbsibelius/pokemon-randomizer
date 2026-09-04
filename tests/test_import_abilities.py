import app.tools.import_abilities as importer
from app.models.ability import Ability


def test_import_ability_transforms_api_data(
    monkeypatch,
) -> None:
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

    def fake_fetch_json(url: str) -> dict:
        assert url.endswith("/ability/1")
        return ability_response

    monkeypatch.setattr(
        importer,
        "fetch_json",
        fake_fetch_json,
    )

    ability = importer.import_ability(1)

    assert isinstance(ability, Ability)
    assert ability.id == 1
    assert ability.name == "Stench"
    assert ability.description == "May cause the target to flinch."
