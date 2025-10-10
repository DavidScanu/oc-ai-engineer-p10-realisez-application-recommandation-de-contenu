# Plan de présentation Google Slides - My Content

**Total : 18-19 slides | Durée : ~23 minutes**

---

## **Section 1 : Introduction (2 slides - 2 min)**

### **Slide 1 : Titre**
- Logo My Content
- Titre : "Système de recommandation d'articles - MVP"
- Votre nom + Date
- OpenClassrooms - Projet 10

### **Slide 2 : Contexte & Mission**
- Start-up My Content : encourager la lecture
- Rôle : CTO/Cofondateur avec Samia (CEO)
- Objectif MVP : recommander 5 articles pertinents par utilisateur
- Dataset : Globo.com (portal de nouvelles brésilien)

---

## **Section 2 : Analyse du jeu de données (2 slides - 2-3 min)**

### **Slide 3 : Vue d'ensemble des données**
- **Articles** : 364,047 articles (2006-2018)
  - 461 catégories | 1 éditeur (Globo.com)
  - Longueur moyenne : 191 mots (60% entre 101-200 mots)
- **Utilisateurs** : 322,897 utilisateurs uniques
  - 2,988,181 clics totaux
  - Moyenne : 9.3 clics/utilisateur
- **Période** : 2006-09-27 à 2018-03-13 (11.5 ans)
- **Visuel** : Graphique - Évolution temporelle des publications (pic en 2017 : 155K articles)

**Éléments visuels** :
- Tableau 3 colonnes : Articles | Utilisateurs | Interactions
- Timeline visuelle 2006-2018 avec pic 2017
- Graphique en barres : publications par année

### **Slide 4 : Insights clés et défis identifiés**
- **Couverture limitée** : Seulement 12.6% des articles consultés (46,033 / 364,047)
- **Engagement variable** :
  - Top utilisateur : 1,232 clics (ID 5890)
  - 64.9 clics/article en moyenne (sur articles consultés)
- **Défis pour le système de recommandation** :
  - ⚠️ Cold start utilisateurs (9.3 clics/user en moyenne)
  - ⚠️ Cold start articles (87% jamais consultés)
  - ✅ Catégories riches (461) pour recommandation par contenu
  - ✅ Top utilisateurs actifs pour validation

**Éléments visuels** :
- Diagramme circulaire : 12.6% couverture (articles consultés vs total)
- Bar chart : Top 5 utilisateurs actifs
- Box callouts avec icônes ⚠️ et ✅ pour défis/opportunités

---

## **Section 3 : Approches de modélisation testées (7 slides - 10 min)**

### **Slide 5 : Vue d'ensemble des 4 méthodes**
- Tableau comparatif : Popularité | Contenu | Clustering | Hybride
- Icônes distinctives pour chaque méthode
- Critères : Personnalisation, Cold start, Complexité

**Tableau suggéré** :
| Méthode | Personnalisation | Cold Start | Complexité | Use Case |
|---------|------------------|------------|------------|----------|
| 🔥 Popularité | ⭐ | ✅✅✅ | Simple | Nouveaux users |
| 📖 Contenu | ⭐⭐⭐ | ⚠️ Users | Moyenne | Users actifs |
| 👥 Clustering | ⭐⭐ | ⚠️ | Élevée | Découverte |
| 🎭 Hybride | ⭐⭐⭐ | ✅✅ | Élevée | Production |

### **Slide 6 : Méthode 1 - Popularité normalisée par âge**
- **Principe** : Score = (clics × utilisateurs uniques) / âge_article
- **Boost nouveauté** :
  - ×1.5 si <24h
  - ×1.2 si <72h
- **✅ Avantages** :
  - Résout le cold start utilisateurs
  - Détecte les tendances émergentes
  - Rapide et fiable
- **⚠️ Limites** :
  - Peu personnalisé
  - Favorise le mainstream

**Formule affichée** :
```
score = (total_clicks × unique_users) / article_age_hours
if age < 24h: score ×= 1.5
elif age < 72h: score ×= 1.2
```

### **Slide 7 : Méthode 2 - Similarité de contenu (Embeddings)**
- **Principe** :
  - Vecteurs 250D (Sentence-BERT)
  - Cosine similarity entre profil user et articles
  - Profil utilisateur = moyenne embeddings articles lus
- **✅ Avantages** :
  - Fortement personnalisé
  - Cohérence thématique garantie
  - Expliquable
- **⚠️ Limites** :
  - Cold start utilisateurs (nécessite historique)
  - Embeddings requis (364MB)
- **Solution fallback** : Métadonnées (catégories + longueur)

**Schéma** :
```
User History → [Article₁, Article₂, ...] → Embeddings → Mean Vector
                                                            ↓
Recommendable Articles → Embeddings → Cosine Similarity → Top 5
```

### **Slide 8 : Méthode 3 - Clustering utilisateurs (K-means)**
- **Architecture** :
  - 5 segments utilisateurs (K-means)
  - 10+ features comportementales (fréquence, diversité, préférences catégories)
- **Recommandation** : Articles populaires dans le cluster de l'utilisateur
- **✅ Avantages** :
  - Découverte (serendipity)
  - Filtrage collaboratif implicite
  - Segmentation marketing réutilisable
- **⚠️ Limites** :
  - Nécessite historique utilisateur
  - Mise à jour quotidienne des clusters
  - Moins personnalisé que contenu

**Features utilisées** :
- Total clics, articles uniques, diversité catégories
- Sessions moyennes, temps moyen par article
- Top 3 catégories préférées (one-hot encoding)

### **Slide 9 : Méthode 4 - Approche hybride**
- **Formule de pondération** :
  ```
  Score final = 40% clustering + 30% contenu + 20% popularité + 10% diversité
  ```
- **Bonus consensus** : +0.2 si article recommandé par 2+ méthodes
- **✅ Avantages** :
  - Robuste (compense faiblesses individuelles)
  - Équilibre personnalisation/découverte
  - Meilleure couverture catalogue
- **⚠️ Limites** :
  - Plus complexe à maintenir
  - Paramètres à ajuster
  - Temps de calcul légèrement supérieur

**Diagramme de flux** :
```
User ID → [Clustering] → 40%
       → [Content]    → 30%  → Weighted Sum → Deduplication → Top 5
       → [Popularity] → 20%
       → [Diversity]  → 10%
```

### **Slide 10 : Gestion du Cold Start**
- **Nouveaux utilisateurs** (<5 articles lus) :
  - Fallback automatique → Popularité
  - Transparent via métadonnées API
  - Transition progressive vers personnalisation
- **Nouveaux articles** :
  - Boost immédiat : ×1.5 si <24h
  - Endpoint dédié : `/articles/recent`
  - Pendant génération embedding : fallback métadonnées
- **Indicateur visuel** : Badge jaune/vert dans l'interface

**Tableau de décision** :
| Profil utilisateur | Historique | Méthode appliquée | Fallback |
|--------------------|------------|-------------------|----------|
| User 5890 (actif) | 1,232 clics | Hybride | Non |
| User 1 (nouveau) | 2 clics | Popularité | Oui |
| User 12345 (moyen) | 8 clics | Hybride | Non |

### **Slide 11 : Comparaison des performances**
**Tableau récapitulatif** :
| Critère | Popularité | Contenu | Clustering | Hybride |
|---------|------------|---------|------------|---------|
| Personnalisation | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Cold start users | ✅✅✅ | ❌ | ⚠️ | ✅✅ |
| Cold start items | ✅✅ | ⚠️ | ⚠️ | ✅ |
| Scalabilité | ✅✅✅ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| Temps réponse | <50ms | ~100ms | ~80ms | ~150ms |
| Diversité | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

**Conclusion** : Hybride = meilleur compromis pour production
- Combine les forces de chaque méthode
- Résiste aux edge cases
- Adaptatif selon profil utilisateur

---

## **Section 4 : Fonctionnalités de l'application (4 slides - 6 min)**

### **Slide 12 : Architecture technique actuelle**
**Schéma** :
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│  Frontend       │      │   Backend        │      │   Données       │
│  Next.js 15     │◄────►│   FastAPI        │◄────►│   CSV Files     │
│  TypeScript     │ REST │   Python 3.11    │      │   Embeddings    │
│  Tailwind CSS   │      │   scikit-learn   │      │   (Git LFS)     │
└─────────────────┘      └──────────────────┘      └─────────────────┘
   localhost:3000           localhost:8000           data/
```

**Technologies** :
- **Frontend** : Next.js 15, TypeScript, Tailwind CSS, shadcn/ui
- **Backend** : Python 3.11, FastAPI, pandas, scikit-learn, Sentence-Transformers
- **Data** : CSV (interactions, articles, metadata) + Pickle (embeddings 250D)

**Déploiement local** :
- Backend : `./backend/start.sh` (port 8000)
- Frontend : `./frontend/start.sh` (port 3000)

### **Slide 13 : Backend - API REST**
**Endpoints principaux** :
```python
POST   /recommend/{user_id}          # Recommandations personnalisées
  ?method=hybrid                     # (popularity|content|clustering|hybrid)
  &n_recommendations=5
  &exclude_seen=true

GET    /users/active?limit=20        # Top utilisateurs actifs
GET    /users/{user_id}/stats        # Statistiques utilisateur

GET    /articles/popular?limit=10    # Articles populaires
GET    /articles/recent?hours=48     # Nouveaux articles
         &category_id=281

GET    /debug/config                 # Configuration système
GET    /debug/data-stats             # Statistiques dataset
```

**Architecture backend** :
- **DataLoader singleton** : Gestion centralisée des données (CSV + embeddings)
- **Recommenders** : 4 classes héritant de `BaseRecommender` (ABC)
- **Factory pattern** : `get_recommender(method)` pour instanciation lazy
- **Documentation** : Swagger interactif (`/docs`)
- **Logging** : Structuré avec rotation

### **Slide 14 : Frontend - Interface utilisateur**
**3 pages principales** :
1. **Recommandations** (`/`) :
   - Sélection utilisateur (dropdown top 20 + recherche manuelle)
   - Switch 4 méthodes (tabs)
   - Affichage 5 recommandations avec métadonnées
   - Indicateur fallback (badge vert/jaune)
   - Stats utilisateur en temps réel

2. **Insights** (`/insights`) :
   - Articles populaires (top 10)
   - Articles récents (<48h)
   - Filtres par catégorie

3. **Statistiques** (`/statistics`) :
   - Vue d'ensemble dataset
   - Top 20 utilisateurs actifs

**Composants clés** :
- `UserSelector` : Dropdown + autocomplete
- `MethodSelector` : Tabs Material UI
- `RecommendationCard` : Affichage article (titre, catégorie, date, mots)
- `FallbackAlert` : Indicateur cold start

**Captures d'écran** : Annotations des 3 pages

### **Slide 15 : Démonstration live (ou vidéo)**
**Scénarios de test** :

**1. Utilisateur actif (ID 5890)** :
- Sélection → Méthode hybride
- Résultat : 5 articles personnalisés
- Badge vert : "Recommandations personnalisées"
- Stats : 1,232 clics, 891 articles uniques

**2. Nouvel utilisateur (ID 1)** :
- Sélection → Méthode content/clustering
- Fallback automatique → Popularité
- Badge jaune : "Historique insuffisant, fallback popularité"
- Stats : 2 clics, 2 articles uniques

**3. Switch entre méthodes** :
- User 5890 → Popularité : Articles tendance
- User 5890 → Contenu : Articles similaires historique
- User 5890 → Clustering : Découverte via cluster
- User 5890 → Hybride : Mix équilibré

**4. Navigation Insights** :
- Articles populaires : Top 10 tous temps
- Articles récents : Filtre <48h, catégorie 281 (sport)

---

## **Section 5 : Architecture cible (2 slides - 2 min)**

### **Slide 16 : Architecture cible évolutive**
**Schéma cloud** :
```
┌──────────────┐      ┌─────────────────┐      ┌──────────────────┐
│   Frontend   │      │   Azure         │      │   Data Layer     │
│   Vercel     │◄────►│   Functions     │◄────►│   PostgreSQL     │
│              │ HTTPS│   (API)         │      │   + pgvector     │
└──────────────┘      └─────────────────┘      └──────────────────┘
                             │                          │
                             │                   ┌──────▼──────────┐
                             │                   │  Azure Blob     │
                             │                   │  Storage        │
                             │                   │  (embeddings)   │
                             │                   └─────────────────┘
                             │
                      ┌──────▼──────────┐
                      │  Redis Cache    │
                      │  (scores)       │
                      └─────────────────┘
```

**Composants** :
- **Frontend** : Vercel (CDN global, auto-scaling)
- **API** : Azure Functions (serverless, consumption plan)
- **Base de données** : PostgreSQL + pgvector extension (embeddings)
- **Queue asynchrone** : Azure Service Bus + Celery (génération embeddings)
- **Cache** : Redis (scores précalculés, TTL 1h)
- **Storage** : Azure Blob Storage (modèles, fichiers volumineux)
- **Monitoring** : Application Insights + Prometheus + Grafana

**Gestion nouveaux articles** :
```
Publication → Service Bus Queue → Celery Worker →
Sentence-BERT API (GPU) → PostgreSQL + Redis invalidation
```

**Gestion nouveaux utilisateurs** :
- Cold start initial : Popularité
- Après 5 articles : Transition progressive vers hybride
- Background job : Recalcul profil toutes les 24h

### **Slide 17 : Pipeline d'embeddings en production**
**Workflow complet** :
```
1. Nouvel article publié (API POST /articles)
   ↓
2. Event → Azure Service Bus Queue
   ↓
3. Celery Worker récupère tâche
   ↓
4. Appel API Sentence-BERT (GPU - Azure ML)
   ↓ (50-100ms/article)
5. Stockage PostgreSQL (pgvector) + Azure Blob
   ↓
6. Invalidation cache Redis
   ↓
7. Article disponible pour recommandation
```

**Pendant génération embedding** (délai ~2min) :
- Fallback métadonnées (catégories + longueur)
- Boost nouveauté ×1.5
- Flag `embedding_pending: true` dans DB

**Mise à jour clusters** :
- Recalcul quotidien via Azure Functions Timer Trigger (3h du matin)
- Incremental K-means pour nouveaux users
- Durée : ~10min pour 322K users

**Coûts estimés** :
- Azure Functions : ~$5/mois (1M requêtes)
- PostgreSQL : ~$20/mois (Basic tier)
- Sentence-BERT API : ~$0.10 / 1000 articles (GPU partagé)
- Redis : ~$15/mois (250MB)
- **Total** : ~$40-50/mois

**Optimisations** :
- ACP pour réduire embeddings 250D → 50D (si limites Azure)
- Batch processing embeddings (100 articles/batch)
- Cache warm-up quotidien (top 1000 users)

---

## **Section 6 : Conclusion (2 slides - 1 min)**

### **Slide 18 : Bilan & Livrables**
**✅ Réalisations** :
- MVP fonctionnel avec 4 méthodes de recommandation
- Cold start résolu (utilisateurs + articles)
- Application complète :
  - Backend FastAPI (API REST + Swagger)
  - Frontend Next.js (3 pages interactives)
- Code versionné sur GitHub avec documentation complète
- Architecture cible scalable définie

**📊 Metrics** :
- 322,897 utilisateurs
- 46,033 articles consultés (364K totaux)
- 2,988,181 interactions
- Temps réponse API : <150ms (hybride)
- Coverage : 12.6% → Opportunité croissance

**📦 Livrables** :
1. Application fonctionnelle (local)
2. Scripts déploiement (Git + GitHub)
3. Documentation technique (CLAUDE.md, README.md)
4. Présentation (cette présentation)

### **Slide 19 : Prochaines étapes**
**🚀 Roadmap technique** :
- [ ] **Phase 1 - Déploiement** (2 semaines)
  - Azure Functions (backend API)
  - Vercel (frontend)
  - PostgreSQL + pgvector

- [ ] **Phase 2 - Optimisation** (1 mois)
  - Tests A/B sur 10% utilisateurs (hybride vs content)
  - Fine-tuning pondérations hybrides
  - Monitoring performances (Prometheus)

- [ ] **Phase 3 - Fonctionnalités** (2 mois)
  - Feedback explicite (like/dislike → +0.5/-0.5 score)
  - Notifications push (nouveaux articles catégories favorites)
  - Historique personnalisé (/users/{id}/history)

**🔬 R&D avancée** :
- Modèles séquentiels (GRU/Transformers pour session-based)
- Graph Neural Networks (user-article-category graph)
- Multi-armed bandits (exploration/exploitation)
- Explainability (LIME pour recommendations)

**💡 Business** :
- Acquisition 1000 beta-testeurs (3 mois)
- Partenariats éditeurs (5-10 médias)
- Monétisation : Freemium (5 reco/jour gratuit, illimité premium)

---

## **Répartition du temps (23 min total)**

| Section | Slides | Durée | Timing cumulé |
|---------|--------|-------|---------------|
| 1. Introduction | 1-2 | 2 min | 0:00-2:00 |
| 2. Analyse données | 3-4 | 2-3 min | 2:00-5:00 |
| 3. Modèles testés | 5-11 | 10 min | 5:00-15:00 |
| 4. Fonctionnalités | 12-15 | 6 min | 15:00-21:00 |
| 5. Architecture cible | 16-17 | 2 min | 21:00-23:00 |
| 6. Conclusion | 18-19 | 1 min | 23:00-24:00 |

**Ajustements si soutenance stricte 20 min** :
- Réduire slide 7 (contenu) : 1 min → 30s
- Fusionner slides 16-17 (architecture) : 2 min → 1 min
- Slide 19 (prochaines étapes) : oral uniquement, pas de slide

---

## **Recommandations visuelles**

### **Palette de couleurs**
- **Primaire** : Bleu (#3B82F6) / Violet (#8B5CF6)
- **Secondaire** : Vert (#10B981) / Jaune (#F59E0B)
- **Neutres** : Gris (#6B7280) / Blanc (#FFFFFF)
- **Accents** : Rouge (#EF4444) pour alertes

### **Icônes & Symboles**
- 🔥 Popularité
- 📖 Contenu
- 👥 Clustering
- 🎭 Hybride
- ⚠️ Défis
- ✅ Opportunités
- 🚀 Roadmap

### **Outils de schémas**
- **Architecture** : draw.io, Excalidraw, Lucidchart
- **Graphiques** : Chart.js, Recharts, Google Sheets
- **Mockups** : Captures d'écran réelles annotées (Figma)

### **Typographie**
- **Titres** : Inter Bold, 32-36pt
- **Sous-titres** : Inter Semibold, 24-28pt
- **Corps** : Inter Regular, 18-20pt
- **Code** : Fira Code, 14-16pt

### **Mise en page**
- **Marges** : 40px minimum
- **Hiérarchie** : Max 3 niveaux de bullets
- **Contraste** : Ratio 4.5:1 minimum (WCAG AA)
- **Images** : Qualité HD, compression optimisée

---

## **Conseils de présentation**

### **Préparation**
- [ ] Tester demo app 30 min avant (backend + frontend running)
- [ ] Préparer 3 users de test (5890, 1, 12345)
- [ ] Ouvrir Swagger docs en backup
- [ ] Screenshots de fallback si demo échoue

### **Pendant la soutenance**
- **Rythme** : 1-1.5 min/slide maximum
- **Transitions** : Phrases de liaison ("Maintenant que nous avons vu..., passons à...")
- **Interaction** : Pointer éléments clés avec curseur
- **Timing** : Montre visible, checkpoints à 10 min et 18 min

### **Questions fréquentes anticipées**
1. **Pourquoi hybride et pas juste content ?**
   → Robustesse cold start + diversité résultats

2. **Scalabilité embeddings avec millions d'articles ?**
   → ACP 250D→50D, FAISS index, cache Redis

3. **Coûts Azure en production ?**
   → ~$50/mois pour 10K users, $200/mois pour 100K

4. **Alternative à Azure Functions ?**
   → AWS Lambda, GCP Cloud Functions, ou FastAPI sur Azure App Service

5. **Métrique d'évaluation qualité recommandations ?**
   → Click-through rate (CTR), temps lecture moyen, diversité catalogue

---

**Dernière mise à jour** : 2025-10-10