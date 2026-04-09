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
      <div class="total-block total-net">
        <span class="total-label">Net estimé (−{{ Math.round(result.tax_rate * 100) }}% charges)</span>
        <span class="total-amount">{{ formatPrice(result.net_estimated) }}</span>
      </div>
      <div class="total-block total-ht">
        <span class="total-label">Total HT</span>
        <span class="total-amount">{{ formatPrice(result.total_ht) }}</span>
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
