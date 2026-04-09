<template>
  <n-config-provider :theme-overrides="(themeOverrides as any)">
    <n-global-style />
    <div class="app-shell">
      <header class="app-header">
        <router-link to="/" class="brand">
          <svg class="brand-icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          APLASMA
        </router-link>
        <nav class="app-nav">
          <router-link :to="{ name: 'new' }">Nouveau devis</router-link>
          <router-link :to="{ name: 'history' }">Historique</router-link>
          <router-link :to="{ name: 'materials' }">Catalogue matière</router-link>
          <router-link :to="{ name: 'settings' }">Paramètres</router-link>
        </nav>
      </header>
      <main class="app-main">
        <router-view />
      </main>
    </div>
  </n-config-provider>
</template>

<script setup lang="ts">
const themeOverrides = {
  common: {
    primaryColor: '#ab6715',
    primaryColorHover: '#c97e1f',
    primaryColorPressed: '#8f5510',
    primaryColorSuppl: '#c97e1f',
    bodyColor: '#f5f0eb',
    cardColor: '#fefcf9',
    modalColor: '#fefcf9',
    popoverColor: '#ffffff',
    borderColor: '#e0d8cf',
    borderRadius: '6px',
    textColor1: '#1a1a1a',
    textColor2: '#354046',
    textColor3: '#7a8e96',
    successColor: '#2d7a4f',
    successColorHover: '#389b62',
    successColorPressed: '#236040',
    successColorSuppl: '#389b62',
    infoColor: '#98a5d4',
    infoColorHover: '#adb8dc',
    infoColorPressed: '#8392c4',
    infoColorSuppl: '#adb8dc',
    warningColor: '#d97706',
    warningColorHover: '#e88c1a',
    warningColorPressed: '#c46605',
    warningColorSuppl: '#e88c1a',
    errorColor: '#c0392b',
    errorColorHover: '#d44637',
    errorColorPressed: '#a52f23',
    errorColorSuppl: '#d44637',
    fontFamily: "'Figtree', system-ui, sans-serif",
    fontFamilyMono: "'Space Mono', monospace",
  },
  DataTable: {
    thColor: '#f0ebe3',
    thTextColor: '#7a8e96',
    tdColor: '#fefcf9',
    tdColorHover: '#f7f2ec',
    borderColor: '#e0d8cf',
  },
  Card: {
    color: '#fefcf9',
    borderColor: '#e0d8cf',
  },
}
</script>
