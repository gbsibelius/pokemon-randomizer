import { useState } from 'react'
import type { Pokemon } from './types/pokemon'
import './App.css'

const GENERATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

function App() {
  const [pokemon, setPokemon] = useState<Pokemon[]>([])
  const [excludeLegendaries, setExcludeLegendaries] = useState(false)
  const [excludeMythicals, setExcludeMythicals] = useState(false)
  const [selectedGenerations, setSelectedGenerations] = useState<number[]>([])

  async function handleGenerateClick() {
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
      }),
    },
  )

  const generatedPokemon: Pokemon[] = await response.json()

  setPokemon(generatedPokemon)
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

        <button
          className="generate-button"
          onClick={handleGenerateClick}
        >
          Generate Pokémon
        </button>

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
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}

export default App