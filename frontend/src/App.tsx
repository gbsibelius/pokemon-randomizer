import { useState } from 'react'
import type { Pokemon } from './types/pokemon'
import './App.css'

const GENERATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

function calculateBST(pokemon: Pokemon): number {
  return (
    pokemon.hp +
    pokemon.attack + 
    pokemon.defense +
    pokemon.special_attack +
    pokemon.special_defense +
    pokemon.speed
  )
}

function getPokemonStats(pokemon: Pokemon) {
  return [
    { label: "HP", value: pokemon.hp },
    { label: "ATK", value: pokemon.hp },
    { label: "DEF", value: pokemon.hp },
    { label: "SP. ATK", value: pokemon.hp },
    { label: "SP. DEF", value: pokemon.hp },
    { label: "SPD", value: pokemon.hp },
  ]
}

function App() {
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [pokemon, setPokemon] = useState<Pokemon[]>([])
  const [excludeLegendaries, setExcludeLegendaries] = useState(false)
  const [excludeMythicals, setExcludeMythicals] = useState(false)
  const [selectedGenerations, setSelectedGenerations] = useState<number[]>([])
  const [minBST, setMinBST] = useState<number | null>(null)
  const [maxBST, setMaxBST] = useState<number | null>(null)

  async function handleGenerateClick() {
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/generate',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            count: 3,
            exclude_legendaries: excludeLegendaries,
            exclude_mythicals: excludeMythicals,
            generations:
              selectedGenerations.length === 0
              ? null
              : selectedGenerations,
            min_bst: minBST,
            max_bst: maxBST,
          }),
        },
      )

      if (!response.ok) {
        throw new Error("Unable to generate Pokemon with these filters.")
      }

      const generatedPokemon: Pokemon[] = await response.json()

      setPokemon(generatedPokemon)
    } catch (error) {
      setError(
        error instanceof Error
        ? error.message
        : "An unexpected error occurred."
      )
    } finally {
      setIsLoading(false)
    }
}

function handleGenerationChange(generation: number) {
  setSelectedGenerations((currentGenerations) => {
    if (currentGenerations.includes(generation)) {
      return currentGenerations.filter(
        (currentGeneration) => currentGeneration !== generation,
      )
    }

    return [...currentGenerations, generation]
  })
}

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">Pokémon Randomizer</p>

        <h1>Randomize your starters!</h1>

        <p className="description">
          Generate 3 random Pokémon using customizable filters.
        </p>

        <div className="filter-options">
          <label>
            <input
              type="checkbox"
              checked={excludeLegendaries}
              onChange={(event) =>
                setExcludeLegendaries(event.target.checked)
              }
            />
            Exclude Legendary Pokemon
          </label>

          <label>
            <input
              type="checkbox"
              checked={excludeMythicals}
              onChange={(event) =>
                setExcludeMythicals(event.target.checked)
              }
            />
            Exclude Mythical Pokemon
          </label>
        </div>

        <fieldset className="generation-filter">
          <legend>Generations</legend>

          <div className="generation-options">
            {GENERATIONS.map((generation) => (
              <label
                className="generation-option"
                key={generation}
              >
                <input
                  type="checkbox"
                  checked={selectedGenerations.includes(generation)}
                  onChange={() => handleGenerationChange(generation)}
                />
                
                Gen {generation}
              </label>
            ))}
          </div>
        </fieldset>

        <div className="bst-filter">
          <label>
            Minimum BST

            <input
              type="number"
              min="0"
              value={minBST ?? ''}
              onChange={(event) => {
                const value = event.target.value

                setMinBST(
                  value === ''
                    ? null
                    : Number(value)
                )
              }}
            />
          </label>

          <label>
            Maximum BST

            <input
              type="number"
              min="0"
              value={maxBST ?? ''}
              onChange={(event) => {
                const value = event.target.value

                setMaxBST(
                  value === ''
                    ? null
                    : Number(value)
                )
              }}
            />
          </label>
        </div>

        <button
          className="generate-button"
          onClick={handleGenerateClick}
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : "Generate Pokémon"}
        </button>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <div className="pokemon-results">
          {pokemon.map((entry) => (
            <div
              className="pokemon-result"
              key={entry.pokedex_number}
            >
              <h2>{entry.name}</h2>

              <p>
                {entry.types.join(' / ')}
              </p>

              <p>
                Generation {entry.generation}
              </p>

              <div className="pokemon-stats">
                {getPokemonStats(entry).map((stat) => (
                  <div
                    className="stat-row"
                    key={stat.label}
                  >
                    <span>{stat.label}</span>
                    <span>{stat.value}</span>
                  </div>
                ))}
              </div>

              <p>
                BST: {calculateBST(entry)}
              </p>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

export default App