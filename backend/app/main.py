from fastapi import FastAPI

app = FastAPI(title="Pokemon Randomizer API")


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a basic status message for the API."""
    return {"message": "Pokemon Randomizer API is running"}