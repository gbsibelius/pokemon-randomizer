import { useEffect, useState } from 'react'
import type { Pokemon } from './types/pokemon'
import type { GenerateRequest } from './types/generateRequest'
import { generatePokemon } from './services/pokemonApi'
import PokemonCard from './components/PokemonCard'
import FilterPanel from './components/FilterPanel'
import './App.css'

type Theme = 'light' | 'dark'

function App() {
  const [theme, setTheme] = useState<Theme>(() => {
    const savedTheme = localStorage.getItem('theme')

    if (savedTheme === 'light' || savedTheme === 'dark') {
      return savedTheme
    }

    return 'light'
  })
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [pokemon, setPokemon] = useState<Pokemon[]>([])
  const [excludeLegendaries, setExcludeLegendaries] = useState(false)
  const [excludeMythicals, setExcludeMythicals] = useState(false)
  const [selectedGenerations, setSelectedGenerations] = useState<number[]>([])
  const [minBST, setMinBST] = useState<number | null>(null)
  const [maxBST, setMaxBST] = useState<number | null>(null)

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('theme', theme)
  }, [theme])

  function handleThemeToggle() {
    setTheme((currentTheme) =>
      currentTheme === 'light'
        ? 'dark'
        : 'light'
    )
  }

  async function handleGenerateClick() {
    setIsLoading(true)
    setError(null)

    try {
      const request: GenerateRequest = {
        count: 3,
        generations:
          selectedGenerations.length === 0
            ? null
            : selectedGenerations,
        exclude_legendaries: excludeLegendaries,
        exclude_mythicals: excludeMythicals,
        min_bst: minBST,
        max_bst: maxBST,
      }
      const generatedPokemon = await generatePokemon(request)

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
        <button
          className="theme-toggle"
          onClick={handleThemeToggle}
        >
          {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
        </button>
        <p className="eyebrow">Pokémon Randomizer</p>

        <h1>Randomize your starters!</h1>

        <p className="description">
          Generate 3 random Pokémon using customizable filters.
        </p>

        <FilterPanel
          excludeLegendaries={excludeLegendaries}
          excludeMythicals={excludeMythicals}
          selectedGenerations={selectedGenerations}
          minBST={minBST}
          maxBST={maxBST}
          onExcludeLegendariesChange={setExcludeLegendaries}
          onExcludeMythicalsChange={setExcludeMythicals}
          onGenerationChange={handleGenerationChange}
          onMinBSTChange={setMinBST}
          onMaxBSTChange={setMaxBST}
        />

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
            <PokemonCard
              key={entry.pokedex_number}
              pokemon={entry}
            />
          ))}
        </div>
      </section>
    </main>
  )
}

export default App