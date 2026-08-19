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
    assert "hp" in pokemon[0]
    assert "attack" in pokemon[0]
    assert "defense" in pokemon[0]
    assert "special_attack" in pokemon[0]
    assert "special_defense" in pokemon[0]
    assert "speed" in pokemon[0]

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
        item["pokemon"]["generation"] == 2
        for item in pokemon
    )

def test_generate_returns_generated_pokemon() -> None:
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

    assert "pokemon" in pokemon[0]
    assert "is_shiny" in pokemon[0]

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
        item["pokemon"]["pokedex_number"]
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

def test_generate_returns_pokemon_within_bst_range() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 3,
            "generations": None,
            "exclude_legendaries": False,
            "exclude_mythicals": False,
            "min_bst": 300,
            "max_bst": 400,
        },
    )

    assert response.status_code == 200

    pokemon = response.json()

    assert len(pokemon) == 3

    for entry in pokemon:
        bst = (
            entry["pokemon"]["hp"]
            + entry["pokemon"]["attack"]
            + entry["pokemon"]["defense"]
            + entry["pokemon"]["special_attack"]
            + entry["pokemon"]["special_defense"]
            + entry["pokemon"]["speed"]
        )

        assert 300 <= bst <= 400

def test_generate_rejects_invalid_bst_range() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 3,
            "min_bst": 600,
            "max_bst": 300,
        },
    )

    assert response.status_code == 422

def test_generate_excludes_mythical_pokemon() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 5,
            "exclude_mythicals": True,
        },
    )

    assert response.status_code == 200

    pokemon = response.json()

    assert all(
        not entry["pokemon"]["is_mythical"]
        for entry in pokemon
    )

def test_generate_rejects_invalid_shiny_chance() -> None:
    response = client.post(
        "/generate",
        json={
            "count": 3,
            "shiny_chance": 101,
        },
    )

    assert response.status_code == 422

def test_generate_excludes_requested_pokedex_numbers() -> None:
    excluded_numbers = [1, 25, 150]

    response = client.post(
        "/generate",
        json={
            "count": 3,
            "exclude_pokedex_numbers": excluded_numbers,
        },
    )

    assert response.status_code == 200

    generated_pokemon = response.json()

    assert all(
        result["pokemon"]["pokedex_number"]
        not in excluded_numbers
        for result in generated_pokemon
    )