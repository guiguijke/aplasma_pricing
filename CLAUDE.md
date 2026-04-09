# aplasma_pricing — Outil de chiffrage métallurgie

## Contexte projet
Outil de chiffrage web auto-hébergé pour Guillaume (auto-entrepreneur en découpe plasma CNC, soudure TIG/MIG-MAG, gravure laser MOPA 60W, scan 3D).
Activité secondaire/passion. Objectif : calculer un prix de vente fiable + estimer le bénéfice net après charges auto-entrepreneur.

## Stack
- **Backend** : Python 3.12 + FastAPI + SQLAlchemy + SQLite
- **Frontend** : Vue.js 3 + Vite + TypeScript + Naive UI + Pinia
- **Déploiement** : Docker Compose sur homelab
- **Ports** : Frontend `3500`, Backend `8500`

## Structure
```
backend/
  main.py              # FastAPI entry point
  database.py          # SQLAlchemy + SQLite setup
  models.py            # ORM: Quote, Material, Config
  schemas.py           # Pydantic validation
  routers/
    config.py          # GET/PUT /api/config
    materials.py       # CRUD /api/materials
    quotes.py          # POST /api/calculate + CRUD /api/quotes
  calculators/
    plasma.py          # Découpe plasma (matière + découpe + perçages)
    welding.py         # Soudure TIG / MIG-MAG
    laser.py           # Gravure MOPA 60W
    scanning.py        # Scan 3D + Plans CAO
    post_process.py    # Nettoyage, décapage Corten, peinture, autre
    material_estimator.py  # Estimation prix par poids quand prix manquant

frontend/src/
  api/index.ts         # Toutes les fonctions d'appel API
  stores/
    config.ts          # Config Pinia (taux, prix...)
    quote.ts           # État du devis en cours
  views/
    NewQuote.vue       # Formulaire de création
    QuoteResult.vue    # Résultat + enregistrement
    History.vue        # Historique des devis
    Settings.vue       # Configuration des taux
    Materials.vue      # Catalogue matière
  components/
    modules/           # Un composant par type d'activité
    ui/
      SliderInput.vue  # Slider réutilisable avec valeur affichée
      PriceBreakdown.vue  # Tableau de décomposition des prix
```

## Lancer en dev
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8500

# Frontend
cd frontend
npm install
npm run dev   # écoute sur 3500, proxy /api → 8500
```

## Lancer en production (Docker)
```bash
docker-compose up --build
# Accès : http://<ip-homelab>:3500
```

## Données persistées
- SQLite : `data/aplasma.db` (monté en volume Docker, ignoré par git)
- Au premier démarrage : config par défaut + 8 matériaux d'exemple insérés automatiquement

## Calculs clés
- **Plasma** : coût matière + coût découpe (€/m linéaire) + coût perçages (€/perçage)
- **Soudure** : heures × taux horaire × multiplicateur complexité
- **Laser** : (surface × densité × pièces) / laser_speed_factor × taux horaire
- **Scan/CAO** : heures × taux horaire × multiplicateur complexité
- **Net estimé** : total_ht × (1 − tax_rate)
- **Prix matière manquant** : estimation par poids = volume × densité × prix_ref_kg

## Design system
- **Thème** : clair/chaleureux (pas dark) via Naive UI theme-overrides dans `App.vue`
- **Charte graphique** :
  - `#ab6715` Or/Cuivre — couleur primaire, prix, brand
  - `#354046` Gris foncé — fond header/nav
  - `#98a5d4` Bleu lavande — net estimé, états info
  - `#f5f0eb` Beige crème — fond principal
  - `#1a1a1a` Noir texte — texte principal
- **Polices** (Google Fonts, chargées dans `index.html`) :
  - `Syne 600/700/800` — brand, titres de page, headers de modules
  - `Figtree 400/500/600` — corps, navigation, labels
  - `Space Mono 400/700` — prix, mesures, valeurs numériques
- **CSS global** : `frontend/src/assets/style.css` (design tokens CSS variables + classes utilitaires)
- **Module cards** : `.module-card` — fond crème, bordure gauche cuivre 4px, header teinté
- Ne pas revenir au dark theme Naive UI

## Conventions
- Tous les prix sont en **€ HT**
- Les lignes avec prix estimé sont marquées `is_estimated: true` → affichées avec `*`
- Les taux sont tous éditables dans l'écran Paramètres (`/settings`)
- Ne pas ajouter de gestion clients, ni génération PDF (l'utilisateur utilise Abby)
