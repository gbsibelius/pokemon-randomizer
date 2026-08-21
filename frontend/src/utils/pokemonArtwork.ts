import type { Pokemon } from '../types/pokemon'

const OFFICIAL_ARTWORK_BASE_URL =
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork'

export function getPokemonArtworkURL(
  pokemon: Pokemon,
  isShiny: boolean,
): string {
  const artworkPath = isShiny
    ? `${OFFICIAL_ARTWORK_BASE_URL}/shiny`
    : OFFICIAL_ARTWORK_BASE_URL

  return `${artworkPath}/${pokemon.pokedex_number}.png`
}
