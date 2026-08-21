import type { Pokemon } from '../types/pokemon'
import type { GeneratedPokemon } from '../types/generatedPokemon'
import { getPokemonArtworkURL } from '../utils/pokemonArtwork'
import { getTypeIconURL } from '../utils/pokemonTypes'
import './PokemonCard.css'

interface PokemonCardProps {
  generatedPokemon: GeneratedPokemon
  onReroll: () => void
  isLoading: boolean
}

const MAX_VISUAL_STAT = 200

function calculateStatPercentage(stat: number): number {
  return Math.min((stat / MAX_VISUAL_STAT) * 100, 100)
}

function getStatStrengthClass(stat: number): string {
  if (stat < 50) {
    return 'stat-very-low'
  }

  if (stat < 70) {
    return 'stat-low'
  }

  if (stat < 90) {
    return 'stat-average-low'
  }

  if (stat < 120) {
    return 'stat-average-high'
  }

  if (stat < 150) {
    return 'stat-high'
  }

  return 'stat-very-high'
}

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
    { label: 'HP', value: pokemon.hp },
    { label: 'ATK', value: pokemon.attack },
    { label: 'DEF', value: pokemon.defense },
    { label: 'SP. ATK', value: pokemon.special_attack },
    { label: 'SP. DEF', value: pokemon.special_defense },
    { label: 'SPD', value: pokemon.speed },
  ]
}

function PokemonCard({
  generatedPokemon,
  onReroll,
  isLoading,
}: PokemonCardProps) {
  const { pokemon, is_shiny } = generatedPokemon

  return (
    <div
      className="pokemon-result"
    >
      <img
        className="pokemon-artwork"
        src={getPokemonArtworkURL(pokemon, is_shiny)}
        alt={`${pokemon.name} artwork`}
      />

      <h2 className="pokemon-name">
        {pokemon.name}

        {is_shiny && (
          <span
            className="shiny-indicator"
            role="img"
            aria-label="Shiny Pokemon"
            title="Shiny Pokemon"
          >
            ✦
          </span>
        )}
      </h2>

      <div className="pokemon-types">
        {pokemon.types.map((type) => (
          <span
            className={`type-badge type-${type.toLowerCase()}`}
            key={type}
          >
            <img
              className="type-icon"
              src={getTypeIconURL(type)}
              alt=""
            />

            {type}
          </span>
        ))}
      </div>

      <div className="pokemon-stats">
        {getPokemonStats(pokemon).map((stat) => (
          <div
            className="stat-row"
            key={stat.label}
          >
            <span className="stat-label">
              {stat.label}
            </span>

            <span className="stat-value">
              {stat.value}
            </span>

            <div className="stat-bar">
              <div
                className={`stat-bar-fill ${getStatStrengthClass(stat.value)}`}
                style={{
                  width: `${calculateStatPercentage(stat.value)}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>

      <button
        className="reroll-button"
        onClick={onReroll}
        disabled={isLoading}
      >
        Reroll
      </button>

      <div className="pokemon-meta">
        <span>Gen {pokemon.generation}</span>

        <span>BST: {calculateBST(pokemon)}</span>
      </div>
    </div>
  )
}

export default PokemonCard