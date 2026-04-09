<template>
  <div class="page-container-wide">
    <h1 class="page-title">Historique des devis</h1>

    <n-data-table
      :columns="columns"
      :data="quotes"
      :loading="loading"
      :row-key="(row: any) => row.id"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, NButton, NSpace, NTag } from 'naive-ui'
import type { DataTableColumns } from 'naive-ui'
import { getQuotes, getQuote, deleteQuote } from '../api'
import { useQuoteStore } from '../stores/quote'

const router = useRouter()
const message = useMessage()
const store = useQuoteStore()
const quotes = ref<any[]>([])
const loading = ref(false)

function formatPrice(v: number) {
  return v.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })
}

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const columns: DataTableColumns = [
  {
    title: 'Date',
    key: 'created_at',
    width: 110,
    render: (row: any) => formatDate(row.created_at),
  },
  {
    title: 'Référence',
    key: 'reference',
  },
  {
    title: 'Total HT',
    key: 'total_ht',
    width: 130,
    align: 'right',
    render: (row: any) =>
      h('span', { style: "font-family: 'Space Mono', monospace; font-size: 13px; color: #ab6715; font-weight: 700" }, [
        formatPrice(row.total_ht),
        row.has_estimates
          ? h(NTag, { type: 'warning', size: 'tiny', style: 'margin-left:6px' }, { default: () => '*' })
          : null,
      ]),
  },
  {
    title: 'Net estimé',
    key: 'net_estimated',
    width: 130,
    align: 'right',
    render: (row: any) =>
      h('span', { style: "font-family: 'Space Mono', monospace; font-size: 13px; color: #98a5d4; font-weight: 700" },
        formatPrice(row.net_estimated)
      ),
  },
  {
    title: 'Actions',
    key: 'actions',
    width: 140,
    render: (row: any) =>
      h(NSpace, null, {
        default: () => [
          h(NButton, { size: 'tiny', onClick: () => onDuplicate(row.id) }, { default: () => 'Dupliquer' }),
          h(NButton, { size: 'tiny', type: 'error', onClick: () => onDelete(row.id) }, { default: () => 'Supprimer' }),
        ],
      }),
  },
]

async function load() {
  loading.value = true
  try {
    quotes.value = await getQuotes()
  } finally {
    loading.value = false
  }
}

async function onDuplicate(id: number) {
  const quote = await getQuote(id)
  store.loadFromQuote(quote)
  router.push({ name: 'new' })
}

async function onDelete(id: number) {
  await deleteQuote(id)
  message.success('Devis supprimé')
  load()
}

onMounted(load)
</script>
