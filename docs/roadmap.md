# Pokemon Randomizer Roadmap

This document tracks completed v1 features and potential future additions
for the Pokemon Randomizer. Future items are ideas to evaluate rather than
committed requirements.

## V1 Features

- Generate 3 unique random Pokemon.
- Filter by one or more generations.
- Optionally exclude Legendary Pokemon.
- Optionally exclude Mythical Pokemon.
- Filter by minimum and maximum BST.
- Configure shiny probability.
- Display shiny artwork and a shiny indicator.
- Reroll individual Pokemon while preserving the other generated cards.
- Reroll the full generated set.
- Prevent single-card rerolls from returning currently visible species.
- Preserve active filters during rerolls.
- Display:
  - Official artwork
  - Name
  - Type(s) and type icons
  - Generation
  - All six base stats
  - Stat-strength bars
  - BST
- Light and dark themes with saved preference.
- Responsive desktop and mobile layouts.
- Gracefully handle loading and API errors.

## Release / Deployment

- Deploy the FastAPI backend.
- Deploy the React frontend.
- Configure the production API URL.
- Configure production CORS.
- Perform production smoke testing.
- Add the live URL and production screenshots to the README.

## Near-Term Ideas

### Ultra Beast Support

Add metadata that identifies Ultra Beasts and allow users to optionally
exclude them from generation.

Design questions:

- Add `is_ultra_beast` to the Pokemon data/model.
- Determine how Ultra Beast metadata should be populated by the importer.
- Decide whether Ultra Beasts should be independent from the Legendary and
  Mythical filters.

## Seeded / Reproducible Randomization

Allow users to provide or generate a seed so that randomization can be
reproduced.

Potential use case:

Two people using the same seed and settings should be able to reproduce the
same sequence of Pokemon.

### Duplicate Prevention

Investigate deterministic generation that avoids repeated species across
multiple rolls, especially for "Then We Fight"-style sessions.

A seed by itself makes randomness reproducible but does not necessarily
prevent duplicates across separate requests.

Possible designs to investigate:

- Deterministically shuffle the eligible Pokemon pool using the seed, then
  consume Pokemon from that shuffled pool.
- Track previously generated Pokemon during a seeded session.
- Reset/rebuild the pool when filters change.
- Define how single-card rerolls affect the deterministic sequence.

## Longer-Term Ideas

- Allow generation counts other than 3.
- Support alternate Pokemon forms/variants.
- Shareable seed/configuration links.
- Additional filters such as Pokemon type.
- Improved frontend validation and backend error messages.
- Additional creator-focused randomizer tools.