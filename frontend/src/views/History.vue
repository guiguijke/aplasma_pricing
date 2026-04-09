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
import * as XLSX from 'xlsx'
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

async function onExport(id: number) {
  const quote = await getQuote(id)
  const wb = XLSX.utils.book_new()
  const rows: (string | number | null)[][] = []

  rows.push(['APLASMA — Devis'])
  rows.push([])
  rows.push(['Référence', quote.reference])
  rows.push(['Date', formatDate(quote.created_at)])
  if (quote.notes) rows.push(['Notes', quote.notes])
  rows.push([])

  if (quote.lines && quote.lines.length > 0) {
    rows.push(['Poste', 'Prix HT (€)'])
    for (const line of quote.lines) {
      rows.push([line.label + (line.is_estimated ? ' *' : ''), line.amount])
    }
    rows.push([])
    if (quote.has_estimates) {
      rows.push(['* Prix estimé (basé sur poids + type de matière)', null])
      rows.push([])
    }
  }

  rows.push(['TOTAL HT', quote.total_ht])
  rows.push(['Net estimé (après charges)', quote.net_estimated])

  const ws = XLSX.utils.aoa_to_sheet(rows)
  ws['!cols'] = [{ wch: 50 }, { wch: 16 }]

  XLSX.utils.book_append_sheet(wb, ws, 'Devis')

  const safeRef = quote.reference.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_').slice(0, 40)
  const dateStr = new Date(quote.created_at).toLocaleDateString('fr-FR').replace(/\//g, '-')
  XLSX.writeFile(wb, `APLASMA_${safeRef}_${dateStr}.xlsx`)
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
    width: 250,
    render: (row: any) =>
      h(NSpace, { size: 4 }, {
        default: () => [
          h(NButton, { size: 'tiny', type: 'primary', onClick: () => onEdit(row.id) }, { default: () => 'Modifier' }),
          h(NButton, { size: 'tiny', onClick: () => onDuplicate(row.id) }, { default: () => 'Dupliquer' }),
          h(NButton, { size: 'tiny', type: 'info', onClick: () => onExport(row.id) }, { default: () => 'XLS' }),
          h(NButton, { size: 'tiny', type: 'error', onClick: () => onDelete(row.id) }, { default: () => '✕' }),
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

async function onEdit(id: number) {
  const quote = await getQuote(id)
  store.loadFromQuote(quote, true)
  router.push({ name: 'new' })
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
