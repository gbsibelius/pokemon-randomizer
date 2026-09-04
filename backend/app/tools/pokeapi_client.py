import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def fetch_json(url: str) -> dict:
    """Fetch a JSON response from the provided URL."""

    request = Request(
        url,
        headers={
            "User-Agent": "pokemon-randomizer/0.1",
            "Accept": "application/json",
        },
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urlopen(
                request,
                timeout=10,
            ) as response:
                return json.load(response)

        except HTTPError as error:
            if error.code not in {
                429,
                500,
                502,
                503,
                504,
            }:
                raise

            if attempt == MAX_RETRIES:
                raise

            print(
                f"HTTP {error.code}. "
                f"Retrying ({attempt}/{MAX_RETRIES})..."
            )

        except (URLError, TimeoutError) as error:
            if attempt == MAX_RETRIES:
                raise

            print(
                f"Network error: {error}. "
                f"Retrying ({attempt}/{MAX_RETRIES})..."
            )

        time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError("Failed to fetch PokéAPI data.")
