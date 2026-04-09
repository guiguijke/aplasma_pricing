import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getConfig, updateConfigKey } from '../api'

export const useConfigStore = defineStore('config', () => {
  const config = ref<Record<string, unknown>>({})
  const loaded = ref(false)

  async function load() {
    config.value = await getConfig()
    loaded.value = true
  }

  async function save(key: string, value: unknown) {
    await updateConfigKey(key, value)
    config.value[key] = value
  }

  return { config, loaded, load, save }
})
