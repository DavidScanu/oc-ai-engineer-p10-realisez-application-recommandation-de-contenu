# My Content - Frontend

> Interface web moderne pour le système de recommandation de contenu My Content

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-38bdf8?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

## 🎯 Fonctionnalités

### Core Features
- ✅ **Sélection d'utilisateur** : Interface intuitive pour choisir parmi les utilisateurs disponibles
- ✅ **Recommandations personnalisées** : Affichage des 5 meilleurs articles recommandés
- ✅ **Méthodes multiples** : Basculement entre 4 méthodes de recommandation
  - 🎭 **Hybride** : Combinaison intelligente de toutes les méthodes
  - 🔥 **Popularité** : Articles tendances normalisés par âge
  - 📖 **Contenu** : Similarité basée sur les embeddings
  - 👥 **Clustering** : Filtrage collaboratif par segments
- ✅ **Indicateur de fallback** : Alerte visuelle quand une méthode de repli est utilisée
- ✅ **Statistiques utilisateur** : Affichage des métriques clés (interactions, articles lus)

### Features Additionnelles
- 📊 **Page Insights** : Découvrez les articles populaires et récents
  - Top 10 des articles les plus consultés
  - Nouveaux articles des dernières 48h
- 🎨 **Design moderne** : Interface élégante avec Tailwind CSS et shadcn/ui
- 📱 **Responsive** : Optimisé pour desktop, tablette et mobile
- ⚡ **Performance** : Loading states et gestion d'erreurs optimale

## 🚀 Démarrage rapide

### Prérequis

- Node.js 20+ installé
- Backend FastAPI en cours d'exécution sur `http://localhost:8000`

### Installation

```bash
# Se placer dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Copier le fichier d'environnement
cp .env.example .env.local

# Démarrer le serveur de développement
npm run dev
```

L'application sera accessible sur [http://localhost:3000](http://localhost:3000)

## ⚙️ Configuration

### Variables d'environnement

Créez un fichier `.env.local` à la racine du dossier `frontend/` :

```bash
# URL de l'API backend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Pour la production, modifiez cette variable avec l'URL de votre backend déployé (ex: Azure Functions).

## 📂 Structure du projet

```
frontend/
├── app/                    # Pages Next.js (App Router)
│   ├── page.tsx           # Page principale - Recommandations
│   ├── insights/          # Page Analytics
│   │   └── page.tsx
│   ├── layout.tsx         # Layout global
│   └── globals.css        # Styles globaux
├── components/            # Composants React
│   ├── ui/               # Composants UI shadcn/ui
│   │   ├── card.tsx
│   │   ├── button.tsx
│   │   ├── select.tsx
│   │   ├── badge.tsx
│   │   └── tabs.tsx
│   ├── UserSelector.tsx       # Sélecteur d'utilisateur
│   ├── MethodSelector.tsx     # Sélecteur de méthode
│   ├── RecommendationCard.tsx # Card d'article recommandé
│   ├── UserStatsCard.tsx      # Statistiques utilisateur
│   └── FallbackAlert.tsx      # Alerte de fallback
├── lib/                   # Utilitaires et logique métier
│   ├── api.ts            # Client API
│   ├── types.ts          # Types TypeScript
│   └── utils.ts          # Fonctions utilitaires
├── .env.local            # Variables d'environnement (local)
├── .env.example          # Template de config
└── package.json          # Dépendances
```

## 🎨 Technologies utilisées

### Core
- **Next.js 15** : Framework React avec App Router
- **TypeScript** : Typage statique pour plus de robustesse
- **React 19** : Bibliothèque UI moderne

### Styling
- **Tailwind CSS 4** : Framework CSS utility-first
- **shadcn/ui** : Composants UI réutilisables et accessibles
- **Lucide React** : Icônes modernes

### State & Data
- **Fetch API** : Communication avec le backend
- **React Hooks** : useState, useEffect pour la gestion d'état

## 📊 Pages disponibles

### Page principale (/)
Interface de recommandation personnalisée :
- Sélection d'utilisateur
- Choix de la méthode de recommandation
- Affichage des 5 articles recommandés
- Statistiques utilisateur en temps réel
- Indicateur de fallback automatique

### Page Insights (/insights)
Tableau de bord analytique :
- **Articles populaires** : Top 10 des articles avec le meilleur score de popularité
- **Articles récents** : Nouveaux articles des dernières 48h
- Navigation par onglets

## 🔌 Intégration Backend

L'application communique avec le backend FastAPI via le client API (`lib/api.ts`).

### Endpoints utilisés

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Vérification de l'API |
| `GET /users` | Liste des utilisateurs |
| `POST /recommend/{user_id}` | Recommandations |
| `GET /users/{user_id}/stats` | Statistiques utilisateur |
| `GET /articles/popular` | Articles populaires |
| `GET /articles/recent` | Articles récents |

### Exemple de requête

```typescript
import { apiClient } from '@/lib/api';

// Obtenir des recommandations
const recommendations = await apiClient.getRecommendations(
  userId,      // ID utilisateur
  'hybrid',    // Méthode
  5,           // Nombre de recommandations
  true         // Exclure articles déjà vus
);
```

## 🧪 Scripts disponibles

```bash
# Développement
npm run dev          # Démarre le serveur de développement

# Production
npm run build        # Compile l'application
npm start            # Démarre le serveur de production

# Qualité du code
npm run lint         # Vérifie le code avec ESLint
```

## 🚢 Déploiement

### Vercel (Recommandé)

```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
vercel

# Variables d'environnement à configurer sur Vercel :
# NEXT_PUBLIC_API_URL=https://votre-backend-url.azurewebsites.net
```

### Azure Static Web Apps

```bash
# Utiliser Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Build
npm run build

# Deploy avec Azure CLI
az staticwebapp create \
  --name my-content-frontend \
  --resource-group my-content-rg \
  --source .
```

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🎯 Roadmap & Améliorations futures

- [ ] Filtres avancés (catégorie, date)
- [ ] Comparaison côte-à-côte des méthodes
- [ ] Graphiques de performance (Chart.js)
- [ ] Mode sombre / clair
- [ ] Internationalisation (i18n)
- [ ] Tests E2E (Playwright)
- [ ] PWA (Progressive Web App)

## 🐛 Debugging

### Le frontend ne se connecte pas au backend

1. Vérifiez que le backend est lancé : `http://localhost:8000/health`
2. Vérifiez `.env.local` : `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Consultez la console navigateur pour les erreurs CORS

### Les recommandations ne s'affichent pas

1. Vérifiez les logs de la console (`F12`)
2. Testez l'endpoint directement : `curl http://localhost:8000/recommend/5890?method=hybrid`
3. Vérifiez que l'utilisateur a suffisamment d'historique

### Problèmes de style

1. Effacez le cache : `rm -rf .next`
2. Redémarrez le serveur : `npm run dev`
3. Vérifiez que Tailwind est correctement configuré

## 📝 Licence

Ce projet fait partie du parcours AI Engineer d'OpenClassrooms.

## 🙏 Remerciements

- [Next.js](https://nextjs.org/) - Framework React
- [shadcn/ui](https://ui.shadcn.com/) - Composants UI
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS
- [Lucide](https://lucide.dev/) - Icônes

---

**Développé avec ❤️ pour le projet P10 - OpenClassrooms AI Engineer**
