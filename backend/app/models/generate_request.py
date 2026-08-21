from typing_extensions import Self

from pydantic import BaseModel, Field, model_validator


class GenerateRequest(BaseModel):
    """Represents the rules supplied for a random generation request."""

    count: int = Field(default=3, ge=1)
    generations: list[int] | None = None
    exclude_legendaries: bool = False
    exclude_mythicals: bool = False
    min_bst: int | None = Field(default=None, ge=0)
    max_bst: int | None = Field(default=None, ge=0)
    exclude_pokedex_numbers: list[int] | None = None
    shiny_chance: int = Field(default=1, ge=0, le=100)

    @model_validator(mode="after")
    def validate_bst_range(self) -> Self:
        """Ensure the minimum BST does not exceed the maximum."""

        if (
            self.min_bst is not None
            and self.max_bst is not None
            and self.min_bst > self.max_bst
        ):
            raise ValueError(
                "min_bst cannot be greater than max_bst."
            )

        return self