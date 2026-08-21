from pydantic import BaseModel
from app.models.pokemon import Pokemon

class GeneratedPokemon(BaseModel):
    """Represents a randomized Pokemon result"""

    pokemon: Pokemon
    is_shiny: bool