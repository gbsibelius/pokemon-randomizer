import { useState } from 'react'
import type { Pokemon } from './types/pokemon'
import './App.css'

function App() {
  const [pokemon, setPokemon] = useState<Pokemon[]>([])

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
      }),
    },
  )

  const generatedPokemon: Pokemon[] = await response.json()

  setPokemon(generatedPokemon)
}

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">Pokémon Randomizer</p>

        <h1>Randomize your starters!</h1>

        <p className="description">
          Generate 3 random Pokémon using customizable filters.
        </p>

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