<template>
  <n-form-item :label="label">
    <div style="display: flex; align-items: center; gap: 12px; width: 100%">
      <n-slider
        :value="modelValue"
        :min="min"
        :max="max"
        :step="step"
        style="flex: 1"
        @update:value="$emit('update:modelValue', $event)"
      />
      <span class="slider-value-tag">{{ displayValue }}</span>
    </div>
  </n-form-item>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  label: string
  modelValue: number
  min?: number
  max?: number
  step?: number
  suffix?: string
}>(), {
  min: 1.0,
  max: 2.5,
  step: 0.1,
  suffix: '',
})

defineEmits<{ 'update:modelValue': [value: number] }>()

const displayValue = computed(() =>
  props.suffix ? `${props.modelValue}${props.suffix}` : `×${props.modelValue.toFixed(1)}`
)
</script>
