# Ability Randomizer Design

## V1 Goals

- Generate 3 unique abilities.
- Display ability name and description.
- Assign every ability to one of five custom ability tiers.
- Use two-step weighted randomization:
  1. Roll an ability tier.
  2. Select an ability from that tier.
- Support single-card rerolls.
- Support Reroll All.
- Prevent duplicate visible abilities.
- Add a separate Ability Randomizer page.

## Ability Tiers

- Poke Ball — little or no battle value.
- Great Ball — small/general battle benefit.
- Ultra Ball — strong or useful in the right context.
- Master Ball — consistently excellent with little downside.
- Luxury Ball — excessively powerful / potentially banned in randomized battles.

## Data

PokeAPI-managed:
- Ability ID
- Name
- Description

Manually curated:
- Ability ID → Ability Tier

## Stretch Goals

- Tier-specific result animations.
- Tune tier probabilities through playtesting.