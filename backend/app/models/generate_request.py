from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    """Represents the rules supplied for a random generation request."""

    count: int = Field(default=3, ge=1)
    generations: list[int] | None = None
    exclude_legendaries: bool = False
    