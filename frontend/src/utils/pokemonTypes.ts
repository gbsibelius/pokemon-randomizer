import bugIcon from '../assets/types/bug.svg'
import darkIcon from '../assets/types/dark.svg'
import dragonIcon from '../assets/types/dragon.svg'
import electricIcon from '../assets/types/electric.svg'
import fairyIcon from '../assets/types/fairy.svg'
import fightingIcon from '../assets/types/fighting.svg'
import fireIcon from '../assets/types/fire.svg'
import flyingIcon from '../assets/types/flying.svg'
import ghostIcon from '../assets/types/ghost.svg'
import grassIcon from '../assets/types/grass.svg'
import groundIcon from '../assets/types/ground.svg'
import iceIcon from '../assets/types/ice.svg'
import normalIcon from '../assets/types/normal.svg'
import poisonIcon from '../assets/types/poison.svg'
import psychicIcon from '../assets/types/psychic.svg'
import rockIcon from '../assets/types/rock.svg'
import steelIcon from '../assets/types/steel.svg'
import waterIcon from '../assets/types/water.svg'

const TYPE_ICONS: Record<string, string> = {
  bug: bugIcon,
  dark: darkIcon,
  dragon: dragonIcon,
  electric: electricIcon,
  fairy: fairyIcon,
  fighting: fightingIcon,
  fire: fireIcon,
  flying: flyingIcon,
  ghost: ghostIcon,
  grass: grassIcon,
  ground: groundIcon,
  ice: iceIcon,
  normal: normalIcon,
  poison: poisonIcon,
  psychic: psychicIcon,
  rock: rockIcon,
  steel: steelIcon,
  water: waterIcon,
}

export function getTypeIconURL(type: string): string {
  return TYPE_ICONS[type.toLowerCase()]
}