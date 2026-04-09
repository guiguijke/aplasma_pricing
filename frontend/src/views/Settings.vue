<template>
  <div class="page-container">
    <h1 class="page-title">Paramètres</h1>

    <n-spin :show="!configStore.loaded">
      <div style="display: flex; flex-direction: column; gap: 20px">

        <n-card title="Fiscalité auto-entrepreneur">
          <n-form label-placement="left" label-width="220">
            <n-form-item label="Taux de charges (%)">
              <n-input-number
                :value="Math.round((taxRate ?? 0.22) * 100)"
                :min="0" :max="60" :step="1"
                style="width: 160px"
                @update:value="(v: number | null) => save('tax_rate', (v ?? 22) / 100)"
              />
            </n-form-item>
          </n-form>
        </n-card>

        <n-card title="Taux horaires (€/h)">
          <n-form label-placement="left" label-width="220">
            <n-form-item v-for="[key, label] in rateLabels" :key="key" :label="label">
              <n-input-number
                :value="hourlyRates[key] ?? 0"
                :min="0" :step="1"
                style="width: 160px"
                @update:value="(v: number | null) => saveHourlyRate(key, v ?? 0)"
              />
            </n-form-item>
          </n-form>
        </n-card>

        <n-card title="Taux découpe plasma">
          <n-form label-placement="left" label-width="220">
            <n-form-item label="Coût/mètre linéaire (€)">
              <n-input-number
                :value="plasmaRates.cut_per_meter ?? 8"
                :min="0" :step="0.1" :precision="2"
                style="width: 160px"
                @update:value="(v: number | null) => savePlasmaRate('cut_per_meter', v ?? 8)"
              />
            </n-form-item>
            <n-form-item label="Coût par perçage (€)">
              <n-input-number
                :value="plasmaRates.pierce_cost ?? 0.30"
                :min="0" :step="0.05" :precision="3"
                style="width: 160px"
                @update:value="(v: number | null) => savePlasmaRate('pierce_cost', v ?? 0.30)"
              />
            </n-form-item>
          </n-form>
        </n-card>

        <n-card title="Post-traitements (€/m²)">
          <n-form label-placement="left" label-width="260">
            <n-form-item v-for="[key, label] in postLabels" :key="key" :label="label">
              <n-input-number
                :value="postRates[key] ?? 0"
                :min="0" :step="0.5" :precision="2"
                style="width: 160px"
                @update:value="(v: number | null) => savePostRate(key, v ?? 0)"
              />
            </n-form-item>
          </n-form>
        </n-card>

        <n-card title="Matière première">
          <n-form label-placement="left" label-width="260">
            <n-form-item label="Marge sur matière première (%)">
              <n-input-number
                :value="Math.round((materialMargin ?? 0.10) * 100)"
                :min="0" :max="100" :step="1"
                style="width: 160px"
                @update:value="(v: number | null) => save('material_margin', (v ?? 10) / 100)"
              />
            </n-form-item>
          </n-form>
          <p class="settings-hint" style="margin-top: 4px">
            Appliquée automatiquement sur le coût matière dans chaque devis.
            Le net estimé exclut le coût matière (c'est un coût passé, pas du bénéfice).
          </p>
        </n-card>

        <n-card title="Prix de référence matière (€/kg)">
          <p class="settings-hint">
            Valeur de repli si aucun matériau avec prix renseigné n'existe pour ce type.
            Quand des prix sont saisis dans le catalogue, la moyenne calculée est utilisée en priorité.
          </p>
          <n-form label-placement="left" label-width="220">
            <n-form-item v-for="[key, label] in matRefLabels" :key="key" :label="label">
              <div style="display: flex; align-items: center; gap: 16px">
                <n-input-number
                  :value="refPricePerKg[key] ?? 0"
                  :min="0" :step="0.05" :precision="2"
                  style="width: 140px"
                  @update:value="(v: number | null) => saveRefPrice(key, v ?? 0)"
                />
                <div v-if="avgPrices[key]" class="avg-badge">
                  <span class="avg-badge-value">{{ avgPrices[key].avg }} €/kg</span>
                  <span class="avg-badge-detail">
                    moy. calculée ({{ avgPrices[key].count }} réf.)
                    <template v-if="avgPrices[key].count > 1">
                      · {{ avgPrices[key].min }}–{{ avgPrices[key].max }}
                    </template>
                  </span>
                </div>
                <span v-else class="avg-badge-empty">Aucun prix renseigné</span>
              </div>
            </n-form-item>
          </n-form>
        </n-card>

        <n-card title="Gravure laser">
          <n-form label-placement="left" label-width="260">
            <n-form-item label="Vitesse laser (cm²/h à densité 1.0)">
              <n-input-number
                :value="laserSpeed ?? 200"
                :min="1" :step="10"
                style="width: 160px"
                @update:value="(v: number | null) => configStore.save('laser_speed_factor', v ?? 200)"
              />
            </n-form-item>
          </n-form>
        </n-card>

      </div>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useConfigStore } from '../stores/config'
import { getAvgPricePerKg } from '../api'

const configStore = useConfigStore()

const taxRate = computed(() => configStore.config.tax_rate as number)
const materialMargin = computed(() => configStore.config.material_margin as number)
const hourlyRates = computed(() => (configStore.config.hourly_rates as Record<string, number>) ?? {})
const plasmaRates = computed(() => (configStore.config.plasma_rates as Record<string, number>) ?? {})
const postRates = computed(() => (configStore.config.post_process_rates as Record<string, number>) ?? {})
const refPricePerKg = computed(() => (configStore.config.ref_price_per_kg as Record<string, number>) ?? {})
const laserSpeed = computed(() => configStore.config.laser_speed_factor as number)

const avgPrices = ref<Record<string, { avg: number; count: number; min: number; max: number }>>({})

onMounted(async () => {
  try {
    avgPrices.value = await getAvgPricePerKg()
  } catch {
    // silent — no averages to show
  }
})

const rateLabels: [string, string][] = [
  ['welding_tig', 'Soudure TIG'],
  ['welding_mig', 'Soudure MIG/MAG'],
  ['laser', 'Gravure laser MOPA'],
  ['scanning', 'Scan 3D'],
  ['cad', 'Plans CAO'],
]

const postLabels: [string, string][] = [
  ['cleaning_per_m2', 'Nettoyage tôle'],
  ['corten_per_m2', 'Décapage + vieillissement Corten'],
  ['painting_standard_per_m2', 'Peinture standard'],
  ['painting_premium_per_m2', 'Peinture premium'],
]

const matRefLabels: [string, string][] = [
  ['steel_mild', 'Acier doux (S235/S355)'],
  ['corten', 'Acier Corten'],
  ['stainless', 'Inox'],
  ['aluminum', 'Aluminium'],
]

function save(key: string, value: unknown) {
  configStore.save(key, value)
}

function saveHourlyRate(key: string, value: number) {
  configStore.save('hourly_rates', { ...hourlyRates.value, [key]: value })
}

function savePlasmaRate(key: string, value: number) {
  configStore.save('plasma_rates', { ...plasmaRates.value, [key]: value })
}

function savePostRate(key: string, value: number) {
  configStore.save('post_process_rates', { ...postRates.value, [key]: value })
}

function saveRefPrice(key: string, value: number) {
  configStore.save('ref_price_per_kg', { ...refPricePerKg.value, [key]: value })
}
</script>

<style scoped>
.settings-hint {
  font-family: 'Figtree', sans-serif;
  font-size: 13px;
  color: #888;
  margin: 0 0 16px 0;
  line-height: 1.5;
}
.avg-badge {
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.avg-badge-value {
  font-family: 'Space Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  color: #ab6715;
}
.avg-badge-detail {
  font-family: 'Figtree', sans-serif;
  font-size: 11px;
  color: #888;
}
.avg-badge-empty {
  font-family: 'Figtree', sans-serif;
  font-size: 12px;
  color: #bbb;
  font-style: italic;
}
</style>
