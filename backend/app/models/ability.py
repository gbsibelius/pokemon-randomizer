from pydantic import BaseModel


class Ability(BaseModel):
    """Represents a Pokemon ability available to the randomizer."""

    
    id: int
    name: str
    description: str