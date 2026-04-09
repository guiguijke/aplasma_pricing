<template>
  <div class="page-container-wide">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 28px; flex-wrap: wrap; gap: 12px">
      <h1 class="page-title" style="margin-bottom: 0">Catalogue matière</h1>
      <n-button type="primary" @click="openForm(null)">+ Ajouter un matériau</n-button>
    </div>

    <div style="display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap">
      <n-select
        v-model:value="filterType"
        :options="typeOptions"
        clearable
        placeholder="Type de matériau"
        style="width: 200px"
      />
      <n-select
        v-model:value="filterProduct"
        :options="productOptions"
        clearable
        placeholder="Type de produit"
        style="width: 200px"
      />
      <n-select
        v-model:value="filterFinish"
        :options="finishOptions"
        clearable
        placeholder="Finition"
        style="width: 160px"
      />
    </div>

    <n-data-table :columns="columns" :data="filtered" :loading="loading" size="small" />

    <n-modal
      v-model:show="showModal"
      preset="card"
      :title="editId ? 'Modifier le matériau' : 'Ajouter un matériau'"
      style="width: 600px"
    >
      <!-- Auto-generated name preview -->
      <div class="auto-name-preview">
        <span class="auto-name-label">Nom auto-généré</span>
        <span class="auto-name-value">{{ generatedName }}</span>
      </div>

      <n-form ref="formRef" :model="form" label-placement="left" label-width="160">
        <n-form-item label="Matériau" path="material_type">
          <n-select v-model:value="form.material_type" :options="typeOptions" />
        </n-form-item>
        <n-form-item label="Type de produit" path="product_type">
          <n-select v-model:value="form.product_type" :options="productOptions" />
        </n-form-item>
        <n-form-item label="Finition" path="finish">
          <n-select v-model:value="form.finish" :options="finishOptions" />
        </n-form-item>
        <n-form-item label="Épaisseur (mm)" path="thickness_mm">
          <n-input-number v-model:value="form.thickness_mm" :min="0" :precision="1" style="width: 100%" />
        </n-form-item>

        <!-- Dimension fields — adapt to product type -->
        <template v-if="form.product_type === 'sheet'">
          <n-form-item label="Largeur tôle (mm)">
            <n-input-number v-model:value="dimWidth" :min="0" :step="50" style="width: 100%" />
          </n-form-item>
          <n-form-item label="Hauteur tôle (mm)">
            <n-input-number v-model:value="dimHeight" :min="0" :step="50" style="width: 100%" />
          </n-form-item>
        </template>
        <template v-else-if="form.product_type === 'tube'">
          <n-form-item label="Côté A (mm)">
            <n-input-number v-model:value="dimA" :min="0" style="width: 100%" />
          </n-form-item>
          <n-form-item label="Côté B (mm)">
            <n-input-number v-model:value="dimB" :min="0" style="width: 100%" />
          </n-form-item>
        </template>
        <template v-else-if="form.product_type === 'flat_bar'">
          <n-form-item label="Largeur (mm)">
            <n-input-number v-model:value="dimW" :min="0" style="width: 100%" />
          </n-form-item>
        </template>
        <template v-else-if="form.product_type === 'angle'">
          <n-form-item label="Côté (mm)">
            <n-input-number v-model:value="dimW" :min="0" style="width: 100%" />
          </n-form-item>
        </template>
        <template v-else-if="form.product_type === 'channel'">
          <n-form-item label="Hauteur profil (mm)">
            <n-input-number v-model:value="dimW" :min="0" style="width: 100%" />
          </n-form-item>
        </template>
        <template v-else-if="form.product_type === 'round_bar'">
          <n-form-item label="Diamètre (mm)">
            <n-input-number v-model:value="dimW" :min="0" style="width: 100%" />
          </n-form-item>
        </template>

        <n-form-item label="Unité" path="unit">
          <n-select v-model:value="form.unit" :options="unitOptions" />
        </n-form-item>
        <n-form-item label="Prix achat (€/unité)" path="purchase_price">
          <n-input-number
            v-model:value="form.purchase_price"
            :min="0"
            :precision="2"
            placeholder="Laisser vide = estimé par poids"
            style="width: 100%"
          />
        </n-form-item>
        <n-form-item label="Fournisseur" path="supplier">
          <n-input v-model:value="form.supplier" />
        </n-form-item>
        <n-form-item label="Suffixe / Commentaire" path="suffix">
          <n-input v-model:value="form.suffix" placeholder="Ex : lot Leroy Merlin, chute..." />
        </n-form-item>
        <n-form-item label="Notes" path="notes">
          <n-input v-model:value="form.notes" type="textarea" :rows="2" />
        </n-form-item>
      </n-form>
      <template #footer>
        <div style="display: flex; justify-content: flex-end; gap: 8px">
          <n-button @click="showModal = false">Annuler</n-button>
          <n-button type="primary" :loading="saving" @click="onSave">Enregistrer</n-button>
        </div>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h, watch } from 'vue'
import { useMessage, NButton, NSpace, NTag } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { getMaterials, createMaterial, updateMaterial, deleteMaterial } from '../api'

const message = useMessage()
const materials = ref<any[]>([])
const loading = ref(false)
const showModal = ref(false)
const saving = ref(false)
const editId = ref<number | null>(null)
const filterType = ref<string | null>(null)
const filterProduct = ref<string | null>(null)
const filterFinish = ref<string | null>(null)

// ── Options ──────────────────────────────────────────────────────────────────

const typeOptions = [
  { label: 'Acier doux (S235/S355)', value: 'steel_mild' },
  { label: 'Corten', value: 'corten' },
  { label: 'Inox', value: 'stainless' },
  { label: 'Aluminium', value: 'aluminum' },
]

const productOptions = [
  { label: 'Tôle', value: 'sheet' },
  { label: 'Tube', value: 'tube' },
  { label: 'Plat', value: 'flat_bar' },
  { label: 'Cornière', value: 'angle' },
  { label: 'UPN/UPE', value: 'channel' },
  { label: 'Rond', value: 'round_bar' },
  { label: 'Autre', value: 'other' },
]

const finishOptions = [
  { label: 'Brut', value: 'brut' },
  { label: 'DKP (Décapé)', value: 'dkp' },
  { label: 'Galvanisé', value: 'galva' },
  { label: 'Larmé', value: 'larme' },
]

const unitOptions = [
  { label: 'm²', value: 'm2' },
  { label: 'kg', value: 'kg' },
  { label: 'mètre linéaire', value: 'ml' },
]

// ── Short labels for auto-name ───────────────────────────────────────────────

const materialShort: Record<string, string> = {
  steel_mild: 'S235', corten: 'Corten', stainless: 'Inox 304', aluminum: 'Alu 5083',
}
const productShort: Record<string, string> = {
  sheet: 'Tôle', tube: 'Tube', flat_bar: 'Plat', angle: 'Cornière',
  channel: 'UPN', round_bar: 'Rond', other: '',
}
const finishShort: Record<string, string> = {
  brut: 'Brut', dkp: 'DKP', galva: 'Galva', larme: 'Larmé',
}

// ── Form state ───────────────────────────────────────────────────────────────

const emptyForm = () => ({
  name: '',
  material_type: 'steel_mild',
  product_type: 'sheet',
  finish: 'brut',
  thickness_mm: 3 as number | null,
  unit: 'm2',
  purchase_price: null as number | null,
  supplier: '',
  suffix: '',
  notes: '',
})
const form = ref(emptyForm())

// Separate dimension refs — synced to/from form.dimensions via watchers
const dimWidth = ref<number | null>(1000)
const dimHeight = ref<number | null>(2000)
const dimA = ref<number | null>(40)
const dimB = ref<number | null>(40)
const dimW = ref<number | null>(null)

// ── Auto-name generation ─────────────────────────────────────────────────────

const generatedName = computed(() => {
  const parts: string[] = []
  const product = productShort[form.value.product_type] || ''
  const mat = materialShort[form.value.material_type] || ''
  const fin = finishShort[form.value.finish] || ''

  if (product) parts.push(product)
  if (mat) parts.push(mat)
  if (fin && form.value.finish !== 'brut') parts.push(fin)

  const t = form.value.thickness_mm
  const pt = form.value.product_type

  if (pt === 'sheet') {
    if (t) parts.push(`${t}mm`)
    if (dimWidth.value && dimHeight.value) parts.push(`${dimWidth.value}×${dimHeight.value}`)
  } else if (pt === 'tube') {
    if (dimA.value && dimB.value && t) {
      parts.push(`${dimA.value}×${dimB.value}×${t}`)
    } else if (dimA.value && dimB.value) {
      parts.push(`${dimA.value}×${dimB.value}`)
    }
  } else if (pt === 'flat_bar') {
    if (dimW.value && t) parts.push(`${dimW.value}×${t}`)
    else if (dimW.value) parts.push(`${dimW.value}`)
  } else if (pt === 'angle') {
    if (dimW.value && t) parts.push(`${dimW.value}×${dimW.value}×${t}`)
    else if (dimW.value) parts.push(`${dimW.value}×${dimW.value}`)
  } else if (pt === 'channel') {
    if (dimW.value) parts.push(`${dimW.value}`)
    if (t) parts.push(`ép.${t}`)
  } else if (pt === 'round_bar') {
    if (dimW.value) parts.push(`Ø${dimW.value}`)
    if (t) parts.push(`ép.${t}`)
  } else {
    if (t) parts.push(`${t}mm`)
  }

  if (form.value.suffix?.trim()) parts.push(`— ${form.value.suffix.trim()}`)

  return parts.join(' ')
})

// ── Build dimensions JSON from refs ──────────────────────────────────────────

function buildDimensions(): Record<string, number> | null {
  const pt = form.value.product_type
  if (pt === 'sheet' && dimWidth.value && dimHeight.value) return { width: dimWidth.value, height: dimHeight.value }
  if (pt === 'tube' && dimA.value && dimB.value) return { a: dimA.value, b: dimB.value }
  if ((pt === 'flat_bar' || pt === 'angle' || pt === 'channel' || pt === 'round_bar') && dimW.value) return { w: dimW.value }
  return null
}

// ── Load dimension refs from material object ─────────────────────────────────

function loadDimensions(dims: any, productType: string) {
  dimWidth.value = null; dimHeight.value = null
  dimA.value = null; dimB.value = null; dimW.value = null
  if (!dims) return
  if (productType === 'sheet') {
    dimWidth.value = dims.width ?? null
    dimHeight.value = dims.height ?? null
  } else if (productType === 'tube') {
    dimA.value = dims.a ?? null
    dimB.value = dims.b ?? null
  } else {
    dimW.value = dims.w ?? null
  }
}

// Reset dimension refs when product type changes
watch(() => form.value.product_type, () => {
  dimWidth.value = null; dimHeight.value = null
  dimA.value = null; dimB.value = null; dimW.value = null
  // Set sensible defaults for sheets
  if (form.value.product_type === 'sheet') {
    dimWidth.value = 1000; dimHeight.value = 2000
  }
})

// Auto-set unit based on product type
watch(() => form.value.product_type, (pt) => {
  if (pt === 'sheet') form.value.unit = 'm2'
  else if (pt === 'tube' || pt === 'flat_bar' || pt === 'angle' || pt === 'channel' || pt === 'round_bar') form.value.unit = 'ml'
  else form.value.unit = 'kg'
})

// ── Filtering ────────────────────────────────────────────────────────────────

const filtered = computed(() =>
  materials.value.filter(m =>
    (!filterType.value || m.material_type === filterType.value) &&
    (!filterProduct.value || m.product_type === filterProduct.value) &&
    (!filterFinish.value || m.finish === filterFinish.value)
  )
)

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' })
}

// ── Table columns ────────────────────────────────────────────────────────────

const columns: DataTableColumns = [
  { title: 'Nom', key: 'name', ellipsis: { tooltip: true } },
  {
    title: 'Matériau', key: 'material_type', width: 140,
    render: (row: any) => typeOptions.find(t => t.value === row.material_type)?.label ?? row.material_type,
  },
  {
    title: 'Produit', key: 'product_type', width: 100,
    render: (row: any) => productOptions.find(t => t.value === row.product_type)?.label ?? row.product_type,
  },
  {
    title: 'Finition', key: 'finish', width: 90,
    render: (row: any) => {
      const label = finishOptions.find(f => f.value === row.finish)?.label ?? row.finish ?? 'Brut'
      if (row.finish === 'dkp') return h(NTag, { type: 'info', size: 'tiny' }, { default: () => 'DKP' })
      if (row.finish === 'galva') return h(NTag, { type: 'success', size: 'tiny' }, { default: () => 'Galva' })
      if (row.finish === 'larme') return h(NTag, { type: 'warning', size: 'tiny' }, { default: () => 'Larmé' })
      return label
    },
  },
  {
    title: 'Épais.', key: 'thickness_mm', width: 70,
    render: (row: any) => row.thickness_mm ? `${row.thickness_mm}` : '—',
  },
  {
    title: 'Prix', key: 'purchase_price', width: 130, align: 'right',
    render: (row: any) =>
      row.purchase_price != null
        ? h('span', { style: "font-family: 'Space Mono', monospace; font-size: 12px; color: #ab6715; font-weight: 700" },
            `${row.purchase_price} €/${row.unit}`)
        : h(NTag, { type: 'warning', size: 'tiny' }, { default: () => 'Estimé *' }),
  },
  { title: 'MAJ', key: 'updated_at', width: 80, render: (row: any) => formatDate(row.updated_at) },
  {
    title: '', key: 'actions', width: 120,
    render: (row: any) =>
      h(NSpace, null, {
        default: () => [
          h(NButton, { size: 'tiny', onClick: () => openForm(row) }, { default: () => 'Modifier' }),
          h(NButton, { size: 'tiny', type: 'error', onClick: () => onDelete(row.id) }, { default: () => '✕' }),
        ],
      }),
  },
]

// ── Form open/save/delete ────────────────────────────────────────────────────

function openForm(mat: any) {
  if (mat) {
    editId.value = mat.id
    form.value = {
      name: mat.name ?? '',
      material_type: mat.material_type,
      product_type: mat.product_type,
      finish: mat.finish ?? 'brut',
      thickness_mm: mat.thickness_mm,
      unit: mat.unit,
      purchase_price: mat.purchase_price,
      supplier: mat.supplier ?? '',
      suffix: mat.suffix ?? '',
      notes: mat.notes ?? '',
    }
    loadDimensions(mat.dimensions, mat.product_type)
  } else {
    editId.value = null
    form.value = emptyForm()
    dimWidth.value = 1000; dimHeight.value = 2000
    dimA.value = null; dimB.value = null; dimW.value = null
  }
  showModal.value = true
}

async function onSave() {
  saving.value = true
  try {
    const payload = {
      ...form.value,
      name: generatedName.value,
      dimensions: buildDimensions(),
    }
    if (editId.value) {
      await updateMaterial(editId.value, payload)
    } else {
      await createMaterial(payload)
    }
    message.success('Enregistré !')
    showModal.value = false
    await load()
  } catch {
    message.error('Erreur lors de la sauvegarde')
  } finally {
    saving.value = false
  }
}

async function onDelete(id: number) {
  await deleteMaterial(id)
  message.success('Supprimé')
  load()
}

async function load() {
  loading.value = true
  try { materials.value = await getMaterials() }
  finally { loading.value = false }
}

onMounted(load)
</script>

<style scoped>
.auto-name-preview {
  background: #f5f0eb;
  border: 2px solid #ab6715;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.auto-name-label {
  font-family: 'Figtree', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.auto-name-value {
  font-family: 'Space Mono', monospace;
  font-size: 15px;
  font-weight: 700;
  color: #ab6715;
}
</style>
