import type { GenerateRequest } from '../types/generateRequest'
import type { Pokemon } from '../types/pokemon'

const API_BASE_URL = 'http://127.0.0.1:8000'

export async function generatePokemon(
  request: GenerateRequest,
): Promise<Pokemon[]> {
  const response = await fetch(
    `${API_BASE_URL}/generate`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    },
  )

  if (!response.ok) {
    throw new Error(
      'Unable to generate Pokémon with these filters.',
    )
  }

  const generatedPokemon: Pokemon[] = await response.json()

  return generatedPokemon
}