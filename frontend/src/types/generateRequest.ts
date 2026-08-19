export interface GenerateRequest {
  count: number
  generations: number[] | null
  exclude_legendaries: boolean
  exclude_mythicals: boolean
  min_bst: number | null
  max_bst: number | null
  shiny_chance: number
  exclude_pokedex_numbers: number[] | null
}