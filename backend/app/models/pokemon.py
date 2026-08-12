from pydantic import BaseModel


class Pokemon(BaseModel):
    """Represents a Pokemon available to the randomizer."""

    pokedex_number: int
    name: str
    generation: int
    types: list[str]

    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    is_legendary: bool
    is_mythical: bool

    @property
    def bst(self) -> int:
        """Return the Pokemon's base stat total."""

        return (
            self.hp
            + self.attack
            + self.defense
            + self.special_attack
            + self.special_defense
            + self.speed
        )