from enum import Enum


class AbilityTier(str, Enum):
    """Represents a custom battle-strength tier for an ability."""

    POKE_BALL = "poke_ball"
    GREAT_BALL = "great_ball"
    ULTRA_BALL = "ultra_ball"
    MASTER_BALL = "master_ball"
    LUXURY_BALL = "luxury_ball"