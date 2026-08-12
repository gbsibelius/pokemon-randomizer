export interface Pokemon {
  pokedex_number: number
  name: string
  generation: number
  types: string[]

  hp: number
  attack: number
  defense: number
  special_attack: number
  special_defense: number
  speed: number

  is_legendary: boolean
  is_mythical: boolean
}