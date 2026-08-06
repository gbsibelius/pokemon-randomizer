from pydantic import BaseModel


class Pokemon(BaseModel):
    """Represents a Pokemon available to the randomizer."""

    pokedex_number: int
    name: str
    generation: int
    types: list[str]
    is_legendary: bool