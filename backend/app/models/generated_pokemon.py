from pydantic import BaseModel
from app.models.pokemon import Pokemon

class GeneratedPokemon(BaseModel):
    """Represents a generated Pokemon"""

    pokemon: Pokemon
    is_shiny: bool