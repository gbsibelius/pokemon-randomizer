import type { GenerateRequest } from '../types/generateRequest'
import type { GeneratedPokemon } from '../types/generatedPokemon'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export async function generatePokemon(
  request: GenerateRequest,
): Promise<GeneratedPokemon[]> {
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
      'Unable to generate Pokemon with these filters.',
    )
  }

  const generatedPokemon: GeneratedPokemon[] = await response.json()

  return generatedPokemon
}