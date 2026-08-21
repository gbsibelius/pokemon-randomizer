import './FilterPanel.css'

const GENERATIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

interface FilterPanelProps {
  selectedGenerations: number[]
  excludeLegendaries: boolean
  excludeMythicals: boolean
  minBST: number | null
  maxBST: number | null
  shinyChance: number | null

  onGenerationChange: (generation: number) => void
  onExcludeLegendariesChange: (value: boolean) => void
  onExcludeMythicalsChange: (value: boolean) => void
  onMinBSTChange: (value: number | null) => void
  onMaxBSTChange: (value: number | null) => void
  onShinyChanceChange: (value: number | null) => void
}

function parseOptionalNumber(value: string): number | null {
  return value === '' ? null : Number(value)
}

function FilterPanel({
  excludeLegendaries,
  excludeMythicals,
  selectedGenerations,
  minBST,
  maxBST,
  shinyChance,
  onExcludeLegendariesChange,
  onExcludeMythicalsChange,
  onGenerationChange,
  onMinBSTChange,
  onMaxBSTChange,
  onShinyChanceChange,
}: FilterPanelProps) {
  return (
    <div className="filter-panel">
      <div className="filter-options">
        <label>
          <input
            type="checkbox"
            checked={excludeLegendaries}
            onChange={(event) =>
              onExcludeLegendariesChange(event.target.checked)
            }
          />
          Exclude Legendary Pokemon
        </label>

        <label>
          <input
            type="checkbox"
            checked={excludeMythicals}
            onChange={(event) =>
              onExcludeMythicalsChange(event.target.checked)
            }
          />
          Exclude Mythical Pokemon
        </label>
      </div>

      <fieldset className="generation-filter">
        <legend>Generations</legend>

        <div className="generation-options">
          {GENERATIONS.map((generation) => (
            <label
              className="generation-option"
              key={generation}
            >
              <input
                type="checkbox"
                checked={selectedGenerations.includes(generation)}
                onChange={() => onGenerationChange(generation)}
              />

              Gen {generation}
            </label>
          ))}
        </div>
      </fieldset>

      <div className="bst-filter">
        <label>
          Minimum BST

          <input
            type="number"
            min="0"
            value={minBST ?? ''}
            onChange={(event) => {
              onMinBSTChange(parseOptionalNumber(event.target.value))
            }}
          />
        </label>

        <label>
          Maximum BST

          <input
            type="number"
            min="0"
            value={maxBST ?? ''}
            onChange={(event) => {
              onMaxBSTChange(parseOptionalNumber(event.target.value))
            }}
          />
        </label>

        <label>
          Shiny Chance (%)

          <input
            type="number"
            min="0"
            max="100"
            value={shinyChance ?? ''}
            onChange={(event) => {
              onShinyChanceChange(parseOptionalNumber(event.target.value))
            }}
          />
        </label>
        <span className="filter-hint">
          (Default: 1%)
        </span>
      </div>
    </div>
  )
}

export default FilterPanel