<template>
  <div class="module-card">
    <div class="module-card-header">
      <span class="module-card-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
        </svg>
        Post-traitements
      </span>
      <button class="module-card-close" @click="$emit('remove')">×</button>
    </div>
    <div class="module-card-body">
      <div v-for="(item, idx) in items" :key="idx" class="post-item">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px">
          <n-select
            :value="item.subtype"
            :options="subtypeOptions"
            style="width: 240px"
            @update:value="updateItem(idx, 'subtype', $event)"
          />
          <n-button size="tiny" quaternary type="error" @click="removeItem(idx)">✕</n-button>
        </div>

        <n-form label-placement="left" label-width="160">
          <template v-if="item.subtype !== 'custom'">
            <n-form-item label="Surface (m²)">
              <n-input-number
                :value="item.area_m2"
                :min="0"
                :precision="2"
                style="width: 100%"
                @update:value="updateItem(idx, 'area_m2', $event)"
              />
            </n-form-item>
            <template v-if="item.subtype === 'painting'">
              <n-form-item label="Type de peinture">
                <n-radio-group :value="item.paint_type || 'standard'" @update:value="updateItem(idx, 'paint_type', $event)">
                  <n-radio value="standard">Standard</n-radio>
                  <n-radio value="premium">Premium</n-radio>
                </n-radio-group>
              </n-form-item>
            </template>
          </template>

          <template v-else>
            <n-form-item label="Libellé">
              <n-input :value="item.label || ''" @update:value="updateItem(idx, 'label', $event)" />
            </n-form-item>
            <n-form-item label="Montant (€)">
              <n-input-number :value="item.amount || 0" :min="0" :precision="2" style="width: 100%" @update:value="updateItem(idx, 'amount', $event)" />
            </n-form-item>
          </template>
        </n-form>
      </div>

      <n-button dashed block @click="addItem">+ Ajouter un post-traitement</n-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Activity } from '../../stores/quote'

const props = defineProps<{ activity: Activity }>()
const emit = defineEmits<{ update: [patch: Record<string, unknown>]; remove: [] }>()

const items = computed(() => (props.activity.items as any[]) || [])

const subtypeOptions = [
  { label: 'Nettoyage tôle', value: 'cleaning' },
  { label: 'Décapage + vieillissement Corten', value: 'corten' },
  { label: 'Peinture / traitement', value: 'painting' },
  { label: 'Autre (montant libre)', value: 'custom' },
]

function addItem() {
  emit('update', { items: [...items.value, { subtype: 'cleaning', area_m2: 1.0 }] })
}

function removeItem(idx: number) {
  const updated = items.value.filter((_, i) => i !== idx)
  emit('update', { items: updated })
}

function updateItem(idx: number, key: string, value: unknown) {
  const updated = items.value.map((item, i) =>
    i === idx ? { ...item, [key]: value } : item
  )
  emit('update', { items: updated })
}
</script>
