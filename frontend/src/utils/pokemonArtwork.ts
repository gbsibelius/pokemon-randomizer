import type { Pokemon } from '../types/pokemon'

const OFFICIAL_ARTWORK_BASE_URL =
    'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork'

export function getPokemonArtworkURL(
    pokemon: Pokemon,
): string {
    return `${OFFICIAL_ARTWORK_BASE_URL}/${pokemon.pokedex_number}.png`
}