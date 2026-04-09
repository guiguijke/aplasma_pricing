<template>
  <div class="module-card">
    <div class="module-card-header">
      <span class="module-card-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="21 16 21 8 12 3 3 8 3 16 12 21 21 16"/>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
          <line x1="12" y1="22.08" x2="12" y2="12"/>
        </svg>
        {{ title }}
      </span>
      <button class="module-card-close" @click="$emit('remove')">×</button>
    </div>
    <div class="module-card-body">
      <n-form label-placement="left" label-width="200">
        <n-form-item label="Durée estimée (heures)">
          <n-input-number
            :value="activity.hours as number"
            :min="0.25"
            :step="0.25"
            :precision="2"
            style="width: 100%"
            @update:value="update('hours', $event)"
          />
        </n-form-item>

        <SliderInput
          label="Complexité"
          :model-value="activity.complexity as number"
          :min="1.0"
          :max="2.5"
          :step="0.1"
          @update:model-value="update('complexity', $event)"
        />
      </n-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import SliderInput from '../ui/SliderInput.vue'
import type { Activity } from '../../stores/quote'

const props = defineProps<{ activity: Activity }>()
const emit = defineEmits<{ update: [patch: Record<string, unknown>]; remove: [] }>()

const title = computed(() =>
  props.activity.activity_subtype === 'cad' ? 'Plans CAO 3D' : 'Scan 3D'
)

function update(key: string, value: unknown) {
  emit('update', { [key]: value })
}
</script>
