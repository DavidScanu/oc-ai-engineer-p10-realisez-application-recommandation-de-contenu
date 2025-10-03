# My Content Frontend - Features Overview

## 🎯 Fonctionnalités implémentées

### ✅ Core Features (Requises)

#### 1. Sélection d'utilisateur
- **Component**: `UserSelector.tsx`
- **Description**: Dropdown permettant de sélectionner un utilisateur parmi les 100 premiers disponibles
- **Auto-sélection**: Le premier utilisateur est automatiquement sélectionné au chargement
- **UI**: Card avec loader pendant le chargement

#### 2. Recommandations personnalisées
- **Component**: `RecommendationCard.tsx`
- **Description**: Affichage des 5 articles recommandés pour l'utilisateur sélectionné
- **Informations affichées**:
  - ID de l'article
  - Score de recommandation
  - Catégorie
  - Nombre de mots
  - Date de publication
  - Raison de la recommandation (reason)

#### 3. Switch entre méthodes
- **Component**: `MethodSelector.tsx`
- **Description**: 4 onglets permettant de basculer entre les méthodes
- **Méthodes disponibles**:
  - 🎭 **Hybride** (par défaut)
  - 🔥 **Popularité**
  - 📖 **Contenu**
  - 👥 **Clustering**
- **UI**: Tabs avec icônes et descriptions

#### 4. Indicateur de fallback
- **Component**: `FallbackAlert.tsx`
- **Description**: Alerte visuelle indiquant quand une méthode de repli est appliquée
- **États**:
  - ✅ **Vert**: Recommandation normale (méthode demandée utilisée)
  - ⚠️ **Jaune**: Fallback appliqué (avec raison détaillée)
- **Informations**: Méthode demandée → Méthode réelle + raison du fallback

#### 5. Statistiques utilisateur
- **Component**: `UserStatsCard.tsx`
- **Description**: Affichage des métriques clés de l'utilisateur
- **Métriques**:
  - ID utilisateur
  - Nombre d'articles uniques lus
  - Total d'interactions
  - Badge "Nouvel utilisateur" si applicable

### 🚀 Features Additionnelles (Bonus)

#### 6. Page Insights & Analytics
- **Route**: `/insights`
- **Description**: Tableau de bord analytique avec 2 vues
- **Vues disponibles**:

  **a) Articles populaires**
  - Top 10 des articles avec le meilleur score de popularité
  - Informations: Score, utilisateurs uniques, total de clics
  - Tri par popularité décroissante

  **b) Articles récents**
  - Nouveaux articles des dernières 48h
  - Informations: Date de publication, catégorie, temps depuis publication
  - Badge "Nouveau" sur chaque article

#### 7. Navigation
- **Header**: Sticky header avec branding My Content
- **Links**: Navigation entre page principale et Insights
- **Footer**: Informations projet

#### 8. Design & UX

**Design System**
- Tailwind CSS 4 avec thème personnalisé
- shadcn/ui components (Card, Button, Select, Badge, Tabs)
- Palette de couleurs harmonieuse (bleu/violet)
- Responsive design (mobile, tablette, desktop)

**Loading States**
- Spinners pendant le chargement
- États vides avec messages explicites
- Transitions fluides

**Error Handling**
- Logs console pour debugging
- Messages d'erreur utilisateur-friendly
- Gestion des états d'échec

## 📊 Architecture

### Pages
```
/                    → Page principale (recommandations)
/insights            → Page analytics (populaires + récents)
```

### Components Hierarchy
```
HomePage
├── UserSelector
│   └── Select (shadcn/ui)
├── MethodSelector
│   └── Tabs (shadcn/ui)
├── UserStatsCard
│   └── Card (shadcn/ui)
├── FallbackAlert
│   └── Card (shadcn/ui)
└── RecommendationCard (×5)
    └── Card (shadcn/ui)

InsightsPage
├── Tabs (shadcn/ui)
│   ├── PopularArticles (Tab)
│   │   └── ArticleCard (×10)
│   └── RecentArticles (Tab)
│       └── ArticleCard (×10)
```

### API Integration
- **Client**: `lib/api.ts` - Client HTTP avec typage TypeScript
- **Types**: `lib/types.ts` - Interfaces TypeScript pour toutes les données
- **Endpoints utilisés**:
  - `GET /users` - Liste utilisateurs
  - `POST /recommend/{user_id}` - Recommandations
  - `GET /users/{user_id}/stats` - Stats utilisateur
  - `GET /popular` - Articles populaires
  - `GET /articles/recent` - Articles récents

## 🎨 UI/UX Highlights

### Design Patterns
- **Cards** pour tous les contenus (cohérence visuelle)
- **Badges** pour les métadonnées (catégories, scores, statuts)
- **Icons** (Lucide React) pour améliorer la lisibilité
- **Gradients** pour le branding (header, titres)

### Responsive Breakpoints
- Mobile: < 640px (1 colonne)
- Tablet: 640px - 1024px (layout adapté)
- Desktop: > 1024px (3 colonnes sur page principale)

### Accessibility
- Contraste élevé (WCAG AA)
- Tailles de texte lisibles
- Focus states visibles
- Labels sémantiques

## 🔄 User Flow

### Flow principal
1. **Landing** → Auto-sélection du premier utilisateur
2. **Chargement** → Loader pendant fetch des recommandations
3. **Affichage** → 5 recommandations + stats utilisateur
4. **Interaction** → Switch de méthode → Re-fetch automatique
5. **Fallback** → Alerte si cold start détecté

### Flow secondaire (Insights)
1. **Navigation** → Clic sur badge "Insights"
2. **Chargement** → Fetch parallèle (populaires + récents)
3. **Exploration** → Switch entre tabs
4. **Retour** → Clic sur "Retour aux recommandations"

## 📝 Configuration

### Environment Variables
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend URL
```

### Scripts
```bash
npm run dev      # Développement (localhost:3000)
npm run build    # Build production
npm start        # Serveur production
npm run lint     # Vérification code
./start.sh       # Script de démarrage auto
```

## 🚀 Deployment Ready

- ✅ Build production optimisé
- ✅ Variables d'environnement configurables
- ✅ Static export compatible
- ✅ Vercel / Azure Static Web Apps ready
- ✅ Docker-ready (voir README.md)

## 🎯 Métriques

### Performance
- **First Load JS**: ~161 kB (page principale)
- **First Load JS**: ~136 kB (page insights)
- **Build Time**: ~4.5s
- **Static Pages**: 2 (/, /insights)

### Code Quality
- ✅ TypeScript strict mode
- ✅ ESLint configured
- ✅ Pas d'erreurs de build
- ✅ Pas d'erreurs TypeScript
- ✅ Hooks optimisés (useCallback)

---

**Status**: ✅ Toutes les fonctionnalités requises + bonus implémentées
**Quality**: Production-ready
**Documentation**: Complète (README.md + ce fichier)
