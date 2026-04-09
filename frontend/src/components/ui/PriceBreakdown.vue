<template>
  <div>
    <table class="breakdown-table">
      <thead>
        <tr>
          <th>Poste</th>
          <th class="align-right">Montant HT</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(line, i) in result.lines" :key="i">
          <td>
            {{ line.label }}
            <span v-if="line.is_estimated" class="est-badge">* estimé</span>
          </td>
          <td class="align-right amount-cell">{{ formatPrice(line.amount) }}</td>
        </tr>
      </tbody>
    </table>

    <div class="totals-section">
      <div class="total-block total-ht">
        <span class="total-label">Total HT</span>
        <span class="total-amount">{{ formatPrice(result.total_ht) }}</span>
      </div>

      <div v-if="result.material_cost_ht > 0" class="net-detail">
        <div class="net-detail-row">
          <span>Total HT</span>
          <span class="mono">{{ formatPrice(result.total_ht) }}</span>
        </div>
        <div class="net-detail-row deduct">
          <span>− Coût matière</span>
          <span class="mono">{{ formatPrice(result.material_cost_ht) }}</span>
        </div>
        <div class="net-detail-row">
          <span>= Marge brute</span>
          <span class="mono">{{ formatPrice(result.total_ht - result.material_cost_ht) }}</span>
        </div>
        <div class="net-detail-row deduct">
          <span>− Charges ({{ Math.round(result.tax_rate * 100) }}%)</span>
          <span class="mono">{{ formatPrice((result.total_ht - result.material_cost_ht) * result.tax_rate) }}</span>
        </div>
      </div>

      <div class="total-block total-net">
        <span class="total-label">
          Net estimé
          <span v-if="result.material_cost_ht > 0" class="net-hint">(hors matière, −{{ Math.round(result.tax_rate * 100) }}% charges)</span>
          <span v-else class="net-hint">(−{{ Math.round(result.tax_rate * 100) }}% charges)</span>
        </span>
        <span class="total-amount">{{ formatPrice(result.net_estimated) }}</span>
      </div>
    </div>

    <n-alert v-if="result.has_estimates" type="warning" size="small" style="margin-top: 16px">
      <strong>* Prix estimé</strong> — basé sur le poids et le type de matériau.
      Demander le tarif exact à ton fournisseur.
    </n-alert>
  </div>
</template>

<script setup lang="ts">
import type { CalcResult } from '../../stores/quote'

defineProps<{ result: CalcResult }>()

function formatPrice(v: number) {
  return v.toLocaleString('fr-FR', { style: 'currency', currency: 'EUR' })
}
</script>

<style scoped>
.net-detail {
  background: #f5f0eb;
  border-radius: 8px;
  padding: 10px 16px;
  margin: 8px 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.net-detail-row {
  display: flex;
  justify-content: space-between;
  font-family: 'Figtree', sans-serif;
  font-size: 13px;
  color: #555;
}
.net-detail-row.deduct {
  color: #c0392b;
}
.net-detail-row .mono {
  font-family: 'Space Mono', monospace;
  font-size: 12px;
  font-weight: 600;
}
.net-hint {
  font-weight: 400;
  font-size: 12px;
  color: #888;
}
</style>
