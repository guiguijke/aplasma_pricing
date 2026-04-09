import api from './client'

// ── Config ──────────────────────────────────────────────────────────────────
export const getConfig = () => api.get('/config').then(r => r.data)
export const updateConfigKey = (key: string, value: unknown) =>
  api.put(`/config/${key}`, { value }).then(r => r.data)

// ── Materials ────────────────────────────────────────────────────────────────
export const getMaterials = () => api.get('/materials').then(r => r.data)
export const getAvgPricePerKg = () => api.get('/materials/avg-price-kg').then(r => r.data)
export const createMaterial = (data: unknown) =>
  api.post('/materials', data).then(r => r.data)
export const updateMaterial = (id: number, data: unknown) =>
  api.put(`/materials/${id}`, data).then(r => r.data)
export const deleteMaterial = (id: number) =>
  api.delete(`/materials/${id}`)

// ── Quotes ───────────────────────────────────────────────────────────────────
export const calculate = (activities: unknown[], taxRate?: number) =>
  api.post('/calculate', { activities, tax_rate: taxRate ?? null }).then(r => r.data)

export const getQuotes = () => api.get('/quotes').then(r => r.data)
export const getQuote = (id: number) => api.get(`/quotes/${id}`).then(r => r.data)
export const saveQuote = (data: unknown) =>
  api.post('/quotes', data).then(r => r.data)
export const updateQuote = (id: number, data: unknown) =>
  api.put(`/quotes/${id}`, data).then(r => r.data)
export const deleteQuote = (id: number) => api.delete(`/quotes/${id}`)
