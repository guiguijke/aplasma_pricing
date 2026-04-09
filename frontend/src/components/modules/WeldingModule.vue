<template>
  <div class="module-card">
    <div class="module-card-header">
      <span class="module-card-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M12 22a7 7 0 007-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-1.7 4.7-3 6.5-1.3 1.8-3 3.5-3 5.5a7 7 0 007 7z"/>
        </svg>
        Soudure TIG / MIG-MAG
      </span>
      <button class="module-card-close" @click="$emit('remove')">×</button>
    </div>
    <div class="module-card-body">
      <n-form label-placement="left" label-width="200">
        <n-form-item label="Type de soudure">
          <n-radio-group
            :value="activity.weld_type as string"
            @update:value="update('weld_type', $event)"
          >
            <n-radio value="tig">TIG</n-radio>
            <n-radio value="mig_mag">MIG/MAG</n-radio>
          </n-radio-group>
        </n-form-item>

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
import SliderInput from '../ui/SliderInput.vue'
import type { Activity } from '../../stores/quote'

const props = defineProps<{ activity: Activity }>()
const emit = defineEmits<{ update: [patch: Record<string, unknown>]; remove: [] }>()

function update(key: string, value: unknown) {
  emit('update', { [key]: value })
}
</script>
