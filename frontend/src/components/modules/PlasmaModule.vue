<template>
  <div class="module-card">
    <div class="module-card-header">
      <span class="module-card-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
        Découpe plasma
      </span>
      <button class="module-card-close" @click="$emit('remove')">×</button>
    </div>
    <div class="module-card-body">
      <n-form label-placement="left" label-width="200">
        <n-form-item label="Matériau">
          <n-select
            :value="activity.material_id"
            :options="materialOptions"
            filterable
            placeholder="Sélectionner un matériau..."
            @update:value="onMaterialSelect"
          />
        </n-form-item>

        <n-form-item label="Longueur de découpe (mm)">
          <n-input-number
            :value="activity.cut_length_mm as number"
            :min="0"
            style="width: 100%"
            @update:value="update('cut_length_mm', $event)"
          />
        </n-form-item>

        <n-form-item label="Nombre de perçages">
          <n-input-number
            :value="activity.pierce_count as number"
            :min="0"
            style="width: 100%"
            @update:value="update('pierce_count', $event)"
          />
        </n-form-item>

        <n-form-item label="Surface tôle (m²)">
          <n-input-number
            :value="activity.sheet_area_m2 as number"
            :min="0"
            :precision="3"
            style="width: 100%"
            @update:value="update('sheet_area_m2', $event)"
          />
        </n-form-item>

        <n-form-item label="Facturation tôle">
          <n-radio-group
            :value="activity.sheet_billing as string"
            @update:value="update('sheet_billing', $event)"
          >
            <n-radio value="partial">Surface réelle utilisée</n-radio>
            <n-radio value="full">Tôle complète</n-radio>
          </n-radio-group>
        </n-form-item>

        <n-form-item label="Prix matière">
          <n-tag v-if="activity.purchase_price != null" type="success">
            {{ (activity.purchase_price as number).toFixed(2) }} € / {{ activity.unit || 'm²' }}
          </n-tag>
          <n-tag v-else type="warning">
            Prix manquant — sera estimé par le poids
          </n-tag>
        </n-form-item>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Activity } from '../../stores/quote'

const props = defineProps<{
  activity: Activity
  materials: any[]
}>()

const emit = defineEmits<{
  update: [patch: Record<string, unknown>]
  remove: []
}>()

function update(key: string, value: unknown) {
  emit('update', { [key]: value })
}

const materialOptions = computed(() =>
  props.materials.map(m => ({
    label: m.purchase_price
      ? `${m.name} — ${m.purchase_price} €/${m.unit}`
      : `${m.name} — prix manquant *`,
    value: m.id,
  }))
)

function onMaterialSelect(id: number) {
  const mat = props.materials.find(m => m.id === id)
  if (!mat) return
  emit('update', {
    material_id: mat.id,
    material_name: mat.name,
    material_type: mat.material_type,
    product_type: mat.product_type,
    thickness_mm: mat.thickness_mm,
    dimensions: mat.dimensions,
    unit: mat.unit,
    purchase_price: mat.purchase_price,
  })
}
</script>
