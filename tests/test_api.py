from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_root_returns_api_status() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Pokemon Randomizer API is running"
    }

def test_get_pokemon_returns_catalog() -> None:
    response = client.get("/pokemon")

    assert response.status_code == 200

    pokemon = response.json()

    assert len(pokemon) > 0
    assert "pokedex_number" in pokemon[0]
    assert "name" in pokemon[0]
    assert "generation" in pokemon[0]
    assert "types" in pokemon[0]
    assert "is_legendary" in pokemon[0]
    assert "is_mythical" in pokemon[0]

def test_generate_returns_requested_generation() -> None:
    request_body = {
        "count": 3,
        "generations": [2],
        "exclude_legendaries": False,
    }

    response = client.post(
        "/generate",
        json=request_body,
    )

    assert response.status_code == 200

    pokemon = response.json()

    assert len(pokemon) == 3
    assert all(
        item["generation"] == 2
        for item in pokemon
    )

def test_generate_returns_unique_pokemon() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 3,
            "generations": None,
            "exclude_legendaries": False,
        },
    )

    assert response.status_code == 200

    pokemon = response.json()

    pokedex_numbers = [
        item["pokedex_number"]
        for item in pokemon
    ]

    assert len(pokedex_numbers) == len(set(pokedex_numbers))

def test_generate_returns_400_when_request_cannot_be_satisfied() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 1,
            "generations": [],
            "exclude_legendaries": False,
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": (
            "Cannot generate the requested number of Pokemon "
            "with the supplied filters."
        )
    }

def test_generate_rejects_count_less_than_one() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 0,
            "generations": [1],
            "exclude_legendaries": False,
        },
    )

    assert response.status_code == 422