<template>
  <div class="page-container">
    <h1 class="page-title">Nouveau devis</h1>

    <n-form label-placement="left" label-width="170" style="margin-bottom: 28px">
      <n-form-item label="Référence / chantier" required>
        <n-input
          :value="store.reference"
          placeholder="Ex : Portail acier client Dupont"
          size="large"
          @update:value="store.reference = $event"
        />
      </n-form-item>
    </n-form>

    <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px">
      <component
        v-for="activity in store.activities"
        :key="activity.id"
        :is="moduleComponent(activity.type)"
        :activity="activity"
        :materials="materials"
        @update="patch => store.updateActivity(activity.id, patch)"
        @remove="store.removeActivity(activity.id)"
      />
    </div>

    <div style="margin-bottom: 32px">
      <p class="section-label">Ajouter un module</p>
      <div style="display: flex; flex-wrap: wrap; gap: 8px">
        <button
          v-for="btn in addButtons"
          :key="btn.type"
          class="add-module-btn"
          @click="store.addActivity(btn.type)"
        >
          <span class="plus">+</span>
          {{ btn.label }}
        </button>
      </div>
    </div>

    <n-button
      type="primary"
      size="large"
      block
      :disabled="!store.reference || store.activities.length === 0"
      :loading="calculating"
      style="height: 48px; font-weight: 600; letter-spacing: 0.5px"
      @click="onCalculate"
    >
      Calculer le devis
    </n-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useQuoteStore } from '../stores/quote'
import { getMaterials } from '../api'
import PlasmaModule from '../components/modules/PlasmaModule.vue'
import WeldingModule from '../components/modules/WeldingModule.vue'
import LaserModule from '../components/modules/LaserModule.vue'
import ScanningModule from '../components/modules/ScanningModule.vue'
import PostProcessModule from '../components/modules/PostProcessModule.vue'

const router = useRouter()
const message = useMessage()
const store = useQuoteStore()
const materials = ref<any[]>([])
const calculating = ref(false)

const addButtons = [
  { type: 'plasma',       label: 'Découpe plasma' },
  { type: 'welding',      label: 'Soudure TIG/MIG' },
  { type: 'laser',        label: 'Gravure laser' },
  { type: 'scanning',     label: 'Scan 3D' },
  { type: 'cad',          label: 'Plans CAO' },
  { type: 'post_process', label: 'Post-traitement' },
]

const moduleMap: Record<string, any> = {
  plasma: PlasmaModule,
  welding: WeldingModule,
  laser: LaserModule,
  scanning: ScanningModule,
  cad: ScanningModule,
  post_process: PostProcessModule,
}

function moduleComponent(type: string) {
  return moduleMap[type] ?? null
}

onMounted(async () => {
  materials.value = await getMaterials()
})

async function onCalculate() {
  calculating.value = true
  try {
    await store.runCalculate()
    router.push({ name: 'result' })
  } catch (e) {
    message.error('Erreur lors du calcul. Vérifiez que le backend est démarré.')
  } finally {
    calculating.value = false
  }
}
</script>
