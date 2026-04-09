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
    </div>

    <n-data-table :columns="columns" :data="filtered" :loading="loading" size="small" />

    <n-modal
      v-model:show="showModal"
      preset="card"
      :title="editId ? 'Modifier le matériau' : 'Ajouter un matériau'"
      style="width: 560px"
    >
      <n-form ref="formRef" :model="form" label-placement="left" label-width="160">
        <n-form-item label="Nom" path="name" required>
          <n-input v-model:value="form.name" />
        </n-form-item>
        <n-form-item label="Matériau" path="material_type">
          <n-select v-model:value="form.material_type" :options="typeOptions" />
        </n-form-item>
        <n-form-item label="Type de produit" path="product_type">
          <n-select v-model:value="form.product_type" :options="productOptions" />
        </n-form-item>
        <n-form-item label="Épaisseur (mm)" path="thickness_mm">
          <n-input-number v-model:value="form.thickness_mm" :min="0" :precision="1" style="width: 100%" />
        </n-form-item>
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
import { ref, computed, onMounted, h } from 'vue'
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

const emptyForm = () => ({
  name: '', material_type: 'steel_mild', product_type: 'sheet',
  thickness_mm: 3, dimensions: null, unit: 'm2',
  purchase_price: null as number | null, supplier: '', notes: '',
})
const form = ref(emptyForm())

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

const unitOptions = [
  { label: 'm²', value: 'm2' },
  { label: 'kg', value: 'kg' },
  { label: 'mètre linéaire', value: 'ml' },
]

const filtered = computed(() =>
  materials.value.filter(m =>
    (!filterType.value || m.material_type === filterType.value) &&
    (!filterProduct.value || m.product_type === filterProduct.value)
  )
)

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: '2-digit' })
}

const columns: DataTableColumns = [
  { title: 'Nom', key: 'name' },
  {
    title: 'Matériau', key: 'material_type', width: 140,
    render: (row: any) => typeOptions.find(t => t.value === row.material_type)?.label ?? row.material_type,
  },
  {
    title: 'Produit', key: 'product_type', width: 110,
    render: (row: any) => productOptions.find(t => t.value === row.product_type)?.label ?? row.product_type,
  },
  {
    title: 'Épais.', key: 'thickness_mm', width: 80,
    render: (row: any) => row.thickness_mm ? `${row.thickness_mm} mm` : '—',
  },
  {
    title: 'Prix', key: 'purchase_price', width: 140, align: 'right',
    render: (row: any) =>
      row.purchase_price != null
        ? h('span', { style: "font-family: 'Space Mono', monospace; font-size: 12px; color: #ab6715; font-weight: 700" },
            `${row.purchase_price} €/${row.unit}`)
        : h(NTag, { type: 'warning', size: 'tiny' }, { default: () => 'Prix manquant *' }),
  },
  { title: 'MAJ', key: 'updated_at', width: 90, render: (row: any) => formatDate(row.updated_at) },
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

function openForm(mat: any) {
  if (mat) {
    editId.value = mat.id
    form.value = { ...mat }
  } else {
    editId.value = null
    form.value = emptyForm()
  }
  showModal.value = true
}

async function onSave() {
  saving.value = true
  try {
    if (editId.value) {
      await updateMaterial(editId.value, form.value)
    } else {
      await createMaterial(form.value)
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
