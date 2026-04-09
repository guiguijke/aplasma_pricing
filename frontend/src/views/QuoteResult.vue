<template>
  <div class="page-container">
    <div style="display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 28px; gap: 16px; flex-wrap: wrap">
      <div>
        <h1 class="page-title" style="margin-bottom: 4px">Résultat du devis</h1>
        <p style="color: var(--c-text-2); margin: 0; font-size: 15px; padding-left: 16px">
          {{ store.reference }}
        </p>
      </div>
      <n-button @click="router.push({ name: 'new' })" style="margin-top: 2px">
        ← Modifier
      </n-button>
    </div>

    <div v-if="store.result">
      <n-alert
        v-if="store.editingId"
        type="info"
        style="margin-bottom: 20px"
      >
        Modification du devis existant — cliquez sur "Mettre à jour" pour enregistrer les changements.
      </n-alert>

      <n-card style="margin-bottom: 24px">
        <PriceBreakdown :result="store.result" />
      </n-card>

      <n-form-item label="Notes">
        <n-input
          v-model:value="store.notes"
          type="textarea"
          placeholder="Notes libres (facultatif)..."
          :rows="3"
        />
      </n-form-item>

      <div style="display: flex; gap: 12px; margin-top: 20px">
        <n-button
          type="primary"
          size="large"
          :loading="saving"
          style="font-weight: 600"
          @click="onSave"
        >
          {{ store.editingId ? 'Mettre à jour le devis' : 'Enregistrer le devis' }}
        </n-button>
        <n-button size="large" @click="router.push({ name: 'new' })">
          Modifier
        </n-button>
      </div>
    </div>

    <n-empty v-else description="Aucun résultat — retourne au formulaire">
      <template #extra>
        <n-button @click="router.push({ name: 'new' })">Nouveau devis</n-button>
      </template>
    </n-empty>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useQuoteStore } from '../stores/quote'
import { saveQuote, updateQuote } from '../api'
import PriceBreakdown from '../components/ui/PriceBreakdown.vue'

const router = useRouter()
const message = useMessage()
const store = useQuoteStore()
const saving = ref(false)

async function onSave() {
  if (!store.result) return
  saving.value = true
  try {
    const payload = {
      reference: store.reference,
      activities: store.activities,
      total_ht: store.result.total_ht,
      net_estimated: store.result.net_estimated,
      has_estimates: store.result.has_estimates,
      notes: store.notes,
      lines: store.result.lines,
    }
    if (store.editingId) {
      await updateQuote(store.editingId, payload)
      message.success('Devis mis à jour !')
    } else {
      await saveQuote(payload)
      message.success('Devis enregistré !')
    }
    store.reset()
    router.push({ name: 'history' })
  } catch (e) {
    message.error('Erreur lors de la sauvegarde.')
  } finally {
    saving.value = false
  }
}
</script>
