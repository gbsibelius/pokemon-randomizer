from app.tools.import_pokemon import get_generation_number


def test_get_generation_number_extracts_generation() -> None:
    generation_url = "https://pokeapi.co/api/v2/generation/3/"

    result = get_generation_number(generation_url)

    assert result == 3