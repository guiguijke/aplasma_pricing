import { defineStore } from 'pinia'
import { ref } from 'vue'
import { calculate } from '../api'

export interface Activity {
  id: string          // client-side uuid for list key
  type: string
  [key: string]: unknown
}

export interface PriceLine {
  label: string
  amount: number
  is_estimated: boolean
}

export interface CalcResult {
  lines: PriceLine[]
  total_ht: number
  net_estimated: number
  has_estimates: boolean
  tax_rate: number
}

export const useQuoteStore = defineStore('quote', () => {
  const reference = ref('')
  const activities = ref<Activity[]>([])
  const result = ref<CalcResult | null>(null)
  const notes = ref('')

  function addActivity(type: string) {
    const defaults: Record<string, unknown> = { type, id: crypto.randomUUID() }
    if (type === 'plasma') {
      Object.assign(defaults, {
        cut_length_mm: 0, pierce_count: 0,
        material_id: null, material_name: '', material_type: 'steel_mild',
        product_type: 'sheet', thickness_mm: 3, dimensions: null,
        sheet_area_m2: 0, sheet_billing: 'partial', purchase_price: null,
      })
    } else if (type === 'welding') {
      Object.assign(defaults, { weld_type: 'tig', hours: 1, complexity: 1.0 })
    } else if (type === 'laser') {
      Object.assign(defaults, { engraved_area_cm2: 10, density: 0.5, piece_count: 1 })
    } else if (type === 'scanning' || type === 'cad') {
      Object.assign(defaults, { activity_subtype: type, hours: 1, complexity: 1.0 })
    } else if (type === 'post_process') {
      Object.assign(defaults, { items: [] })
    }
    activities.value.push(defaults as Activity)
  }

  function removeActivity(id: string) {
    activities.value = activities.value.filter(a => a.id !== id)
  }

  function updateActivity(id: string, patch: Record<string, unknown>) {
    const idx = activities.value.findIndex(a => a.id === id)
    if (idx !== -1) {
      activities.value[idx] = { ...activities.value[idx], ...patch }
    }
  }

  async function runCalculate() {
    result.value = await calculate(activities.value)
  }

  function reset() {
    reference.value = ''
    activities.value = []
    result.value = null
    notes.value = ''
  }

  function loadFromQuote(quote: { reference: string; activities: Activity[]; notes: string }) {
    reference.value = quote.reference
    activities.value = quote.activities.map(a => ({
      ...a,
      id: crypto.randomUUID(),
    }))
    notes.value = quote.notes
    result.value = null
  }

  return {
    reference, activities, result, notes,
    addActivity, removeActivity, updateActivity, runCalculate, reset, loadFromQuote,
  }
})
