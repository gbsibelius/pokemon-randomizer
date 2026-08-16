import type { Pokemon } from '../types/pokemon'
import './PokemonCard.css'

interface PokemonCardProps {
  pokemon: Pokemon
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
    { label: "HP", value: pokemon.hp },
    { label: "ATK", value: pokemon.attack },
    { label: "DEF", value: pokemon.defense },
    { label: "SP. ATK", value: pokemon.special_attack },
    { label: "SP. DEF", value: pokemon.special_defense },
    { label: "SPD", value: pokemon.speed },
  ]
}

function PokemonCard({ pokemon }: PokemonCardProps) {
  return (
    <div
      className="pokemon-result"
      key={pokemon.pokedex_number}
    >
      <h2>{pokemon.name}</h2>

      <p>
        {pokemon.types.join(' / ')}
      </p>

      <p>
        Generation {pokemon.generation}
      </p>

      <div className="pokemon-stats">
        {getPokemonStats(pokemon).map((stat) => (
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
        BST: {calculateBST(pokemon)}
      </p>
    </div>
  )
}

export default PokemonCard