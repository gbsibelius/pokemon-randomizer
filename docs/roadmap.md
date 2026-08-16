# Pokémon Randomizer Roadmap

This document tracks potential features and larger design ideas for the
Pokémon Randomizer. Items here are not necessarily committed requirements;
they are ideas to evaluate and prioritize as the project develops.

## Current MVP

- Generate 3 unique random Pokémon.
- Filter by one or more generations.
- Optionally exclude Legendary Pokémon.
- Optionally exclude Mythical Pokémon.
- Filter by minimum and maximum BST.
- Display:
  - Name
  - Type(s)
  - Generation
  - Base stats
  - BST
- Gracefully handle loading and API errors.

## Near-Term Features

### Pokémon Card Design

Improve the visual presentation of generated Pokémon.

Potential additions:

- Pokémon artwork or sprites.
- Better stat presentation.
- Visually distinguish BST from individual stats.
- Type-specific styling.
- Responsive/mobile-friendly cards.

### Ultra Beast Support

Add metadata that identifies Ultra Beasts and allow users to optionally
exclude them from generation.

Design questions:

- Add `is_ultra_beast` to the Pokémon data/model.
- Determine how Ultra Beast metadata should be populated by the importer.
- Decide whether Ultra Beasts should be independent from the Legendary and
  Mythical filters.

### Shiny Pokémon

Allow generated results to sometimes be shiny.

Potential behavior:

- Configurable shiny probability.
- Display whether a generated Pokémon is shiny.
- Eventually display shiny artwork when available.

Design question:

A shiny result is a property of a particular generation result rather than
an inherent property of the Pokémon species, so consider introducing a
generated-result/card model rather than adding `is_shiny` directly to the
base `Pokemon` model.

### Rerolling

Allow users to:

- Reroll all generated Pokémon.
- Reroll a single Pokémon card.

Consider how rerolls interact with:

- Current filters.
- Duplicate prevention.
- Seeded generation.
- Shiny rolls.

## Seeded / Reproducible Randomization

Allow users to provide or generate a seed so that randomization can be
reproduced.

Potential use case:

Two people using the same seed and settings should be able to reproduce the
same sequence of Pokémon.

### Duplicate Prevention

Investigate deterministic generation that avoids repeated species across
multiple rolls, especially for "Then We Fight"-style sessions.

A seed by itself makes randomness reproducible but does not necessarily
prevent duplicates across separate requests.

Possible designs to investigate:

- Deterministically shuffle the eligible Pokémon pool using the seed, then
  consume Pokémon from that shuffled pool.
- Track previously generated Pokémon during a seeded session.
- Reset/rebuild the pool when filters change.
- Define how single-card rerolls affect the deterministic sequence.

## Longer-Term Ideas

- Allow generation counts other than 3.
- Support alternate Pokémon forms/variants.
- Shareable seed/configuration links.
- Additional filters such as Pokémon type.
- Improved frontend validation and backend error messages.
- Deployment/public hosting.