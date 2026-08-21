import { useEffect, useState } from 'react'
import type { GeneratedPokemon } from './types/generatedPokemon'
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
  const [generatedPokemon, setGeneratedPokemon] = useState<GeneratedPokemon[]>([])
  const [excludeLegendaries, setExcludeLegendaries] = useState(false)
  const [excludeMythicals, setExcludeMythicals] = useState(false)
  const [selectedGenerations, setSelectedGenerations] = useState<number[]>([])
  const [minBST, setMinBST] = useState<number | null>(null)
  const [maxBST, setMaxBST] = useState<number | null>(null)
  const [shinyChance, setShinyChance] = useState<number | null>(1)
  const generateButtonLabel =
    generatedPokemon.length === 0
      ? 'Generate Pokemon'
      : 'Reroll All'

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

  function buildGenerateRequest(
    count: number,
    excludePokedexNumbers: number[] | null,
  ): GenerateRequest {
    return {
      count,
      generations:
        selectedGenerations.length === 0
          ? null
          : selectedGenerations,
      exclude_legendaries: excludeLegendaries,
      exclude_mythicals: excludeMythicals,
      min_bst: minBST,
      max_bst: maxBST,
      shiny_chance: shinyChance ?? 1,
      exclude_pokedex_numbers: excludePokedexNumbers,
    }
  }

  async function handleGenerateClick() {
    setIsLoading(true)
    setError(null)

    try {
      const request = buildGenerateRequest(3, null)
      const results = await generatePokemon(request)

      setGeneratedPokemon(results)
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

  async function handleReroll(index: number) {
    setIsLoading(true)
    setError(null)

    const excludedNumbers = generatedPokemon.map(
      (result) => result.pokemon.pokedex_number,
    )

    try {
      const request = buildGenerateRequest(1, excludedNumbers)

      const rerollResults = await generatePokemon(request)
      const rerolledPokemon = rerollResults[0]

      if (!rerolledPokemon) {
        throw new Error('Reroll did not return a Pokemon.')
      }

      setGeneratedPokemon((currentPokemon) =>
        currentPokemon.map((result, currentIndex) =>
          currentIndex === index
            ? rerolledPokemon
            : result
        )
      )
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'An unexpected error occurred.'
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
        <p className="eyebrow">Pokemon Randomizer</p>

        <h1>Randomize your starters!</h1>

        <p className="description">
          Generate 3 random Pokemon using customizable filters.
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
          shinyChance={shinyChance}
          onShinyChanceChange={setShinyChance}
        />

        <button
          className="generate-button"
          onClick={handleGenerateClick}
          disabled={isLoading}
        >
          {isLoading ? 'Generating...' : generateButtonLabel}
        </button>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <div className="pokemon-results">
          {generatedPokemon.map((result, index) => (
            <PokemonCard
              key={result.pokemon.pokedex_number}
              generatedPokemon={result}
              onReroll={() => handleReroll(index)}
              isLoading={isLoading}
            />
          ))}
        </div>
      </section>
    </main>
  )
}

export default App