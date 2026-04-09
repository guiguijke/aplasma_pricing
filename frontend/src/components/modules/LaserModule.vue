<template>
  <div class="module-card">
    <div class="module-card-header">
      <span class="module-card-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10"/>
          <circle cx="12" cy="12" r="3"/>
          <line x1="12" y1="2" x2="12" y2="5"/>
          <line x1="12" y1="19" x2="12" y2="22"/>
          <line x1="2" y1="12" x2="5" y2="12"/>
          <line x1="19" y1="12" x2="22" y2="12"/>
        </svg>
        Gravure laser MOPA 60W
      </span>
      <button class="module-card-close" @click="$emit('remove')">×</button>
    </div>
    <div class="module-card-body">
      <n-form label-placement="left" label-width="200">
        <n-form-item label="Surface gravée (cm²)">
          <n-input-number
            :value="activity.engraved_area_cm2 as number"
            :min="0.1"
            :precision="1"
            style="width: 100%"
            @update:value="update('engraved_area_cm2', $event)"
          />
        </n-form-item>

        <SliderInput
          label="Densité du motif"
          :model-value="activity.density as number"
          :min="0.1"
          :max="1.0"
          :step="0.05"
          suffix=""
          @update:model-value="update('density', $event)"
        />

        <n-form-item label="Nombre de pièces">
          <n-input-number
            :value="activity.piece_count as number"
            :min="1"
            :step="1"
            style="width: 100%"
            @update:value="update('piece_count', $event)"
          />
        </n-form-item>
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import SliderInput from '../ui/SliderInput.vue'
import type { Activity } from '../../stores/quote'

const props = defineProps<{ activity: Activity }>()
const emit = defineEmits<{ update: [patch: Record<string, unknown>]; remove: [] }>()

function update(key: string, value: unknown) {
  emit('update', { [key]: value })
}
</script>
