# Projet 10 : Réalisez une application de recommandation de contenu

## Contexte

## Mission 

## Livrables 

## Plan d'action


## Analyse exploratoire des données

Cette section présente l'analyse exploratoire des données du portail de news Globo.com, comprenant les interactions utilisateurs et les métadonnées des articles.

### Vue d'ensemble du dataset

Le dataset est composé de trois éléments principaux :
- **Interactions utilisateurs** : Fichiers de clics organisés par heure (`clicks_hour_*.csv`)
- **Métadonnées des articles** : Informations sur 364K+ articles (`articles_metadata.csv`)
- **Embeddings des articles** : Représentations vectorielles de 250 dimensions (`articles_embeddings.pickle`)

### Analyse des interactions utilisateurs et des métadonnées des articles

```bash
# Comander pour exécuter l'analyse
python3 backend/data-analysis/analyze_data.py
```

**Résultats clés :**
- 👥 **322,897 utilisateurs uniques**
- 📄 **46,033 articles consultés** (sur 364K disponibles)
- 🖱️ **2,988,181 clics** au total
- 📊 **9.3 clics/utilisateur** en moyenne
- 📊 **64.9 clics/article** en moyenne
- 📁 **385 fichiers horaires** de données

#### Informations générales
- 📄 **364,047 articles** au total
- 📊 **5 colonnes** : `article_id`, `category_id`, `created_at_ts`, `publisher_id`, `words_count`
- 💾 **13.9 MB** en mémoire
- ✅ **Aucune valeur manquante**
- 🆔 **IDs uniques** : de 0 à 364,046 (séquentiels)

#### Évolution temporelle
- 📅 **Période couverte** : 2006-09-27 à 2018-03-13 (4,185 jours)
- 📈 **Croissance exponentielle** :
  - 2006-2012 : 634 articles (démarrage)
  - 2013-2016 : 161,104 articles (développement)
  - 2017-2018 : 202,309 articles (55.6% du total)
- ⚠️ **Arrêt brutal** : Mars 2018 (8 articles seulement)

#### Distribution par catégories
- 🏷️ **461 catégories** différentes
- 📊 **Distribution équilibrée** : Top catégorie = 3.5% seulement
- 📈 **Top 10 représentent 23.1%** du total :
  - Catégorie 281: 12,817 articles (3.5%)
  - Catégorie 375: 10,005 articles (2.7%)
  - Catégorie 399: 9,049 articles (2.5%)
  - Catégorie 412: 8,648 articles (2.4%)
  - Catégorie 431: 7,759 articles (2.1%)
  - Catégorie 428: 7,731 articles (2.1%)
  - Catégorie 26: 7,343 articles (2.0%)
  - Catégorie 7: 6,726 articles (1.8%)
  - Catégorie 299: 6,634 articles (1.8%)
  - Catégorie 301: 6,446 articles (1.8%)
- 📊 **Longue traîne** : Médiane de 36 articles par catégorie

#### Caractéristiques des articles
- 📰 **1 éditeur** unique (Globo.com)
- 📝 **191 mots** en moyenne par article
- 📊 **Distribution homogène** :
  - 60.2% des articles : 101-200 mots
  - 34.9% des articles : 201-300 mots
  - 95.1% des articles : 100-300 mots (très cohérent)

### Points clés pour la recommandation

**Avantages :**
- ✅ Dataset complet sans valeurs manquantes
- ✅ Distribution équilibrée des catégories (pas de monopole)
- ✅ Articles homogènes en longueur (cohérence qualitative)
- ✅ Données récentes et denses (2017-2018)
- ✅ Bon ratio utilisateurs/articles pour le filtrage collaboratif
- ✅ IDs séquentiels (facilite l'indexation)

**Défis identifiés :**
- ⚠️ **Cold start** : Seulement 12.6% des articles ont été consultés
- ⚠️ **Sparsité** : Moyenne de 9.3 clics/utilisateur (interactions limitées)
- ⚠️ **Articles très courts** : 1% des articles < 50 mots
- ⚠️ **Concentration temporelle** récente (biais potentiel vers 2017-2018)
- ⚠️ **Arrêt de publication** en mars 2018 (données figées)

Ces insights guideront la conception des algorithmes de recommandation, notamment pour gérer le problème de cold start et optimiser l'équilibre entre popularité et diversité des recommandations.

### 📊 Insights clés pour les recommandeurs

#### ✅ **Points positifs**
- **Dataset complet** : 364K articles, aucune valeur manquante
- **Catégories bien distribuées** : 461 catégories (pas de sur-concentration)
- **Articles homogènes** : 95% entre 100-300 mots (cohérent)
- **Période récente** : Pic en 2017-2018 (données fraîches)

#### ⚠️ **Points d'attention pour nos recommandeurs**
- **Un seul éditeur** : Pas de diversification par source
- **Concentration temporelle** : 2017-2018 = 55% des articles
- **Articles très courts** : 3,729 articles < 50 mots (à filtrer)

---

# Backend FastAPI

## Fonctionnalités implémentées

### Système de recommandation multi-approches

L'application implémente **4 méthodes de recommandation** complémentaires :

- **🔥 Popularité normalisée par âge** : Recommande les articles avec le meilleur ratio clics/mois d'existence (favorise les tendances récentes)
- **📖 Similarité de contenu** : Utilise les embeddings pour recommander des articles similaires à ceux déjà lus
- **👥 Clustering d'utilisateurs** : Segmente les utilisateurs en 5 groupes et recommande les articles populaires dans chaque segment
- **🎭 Hybride** : Combine intelligemment les 3 approches précédentes avec pondération (40% clustering, 30% contenu, 20% popularité, 10% diversité)

#### Calcul de popularité normalisée

Le système utilise une approche innovante pour calculer la popularité en **normalisant par l'âge de l'article** :

**Formule** :
```
popularity_score = (0.7 × unique_users + 0.3 × total_clicks) / article_age_months
```

**Avantages** :
- ✅ **Équité temporelle** : Les nouveaux articles ne sont pas désavantagés par rapport aux anciens
- ✅ **Détection de tendances** : Un article récent avec peu de clics peut surpasser un ancien avec beaucoup de clics s'il a un meilleur ratio
- ✅ **Pas de fenêtre arbitraire** : Plus besoin de définir une fenêtre fixe (ex: 90 jours)

**Exemple** :
```
Article A (8 mois) : 800 clics → score = 800/8 = 100 clics/mois
Article B (1 mois)  : 150 clics → score = 150/1 = 150 clics/mois
→ Article B est considéré comme plus "populaire" car plus tendance
```

**Protection** : Un âge minimum de 0.5 mois est appliqué pour éviter des scores artificiellement élevés sur des articles publiés il y a quelques jours.

#### Similarité de contenu avec embeddings

- **Embeddings pré-calculés** : Vecteurs de 250 dimensions pour chaque article
- **Mesure de similarité** : Cosine similarity pour trouver les articles les plus proches
- **Recommandations personnalisées** : Basées sur l'historique de lecture de l'utilisateur
- **Filtrage qualité** : Exclusion des articles trop courts (< 50 mots) ou trop anciens (> 2 ans)

#### Clustering d'utilisateurs

- **Segmentation** : Les utilisateurs sont regroupés en 5 clusters basés sur leurs comportements de lecture
- **Recommandations par cluster** : Les articles populaires dans chaque cluster sont recommandés aux utilisateurs
- **Adaptabilité** : Permet de recommander des articles même pour les utilisateurs avec peu d'historique

#### Approche hybride

- **Combinaison pondérée** des scores des 3 méthodes précédentes
- **Pondérations** : 40% clustering, 30% contenu, 20% popularité, 10% diversité
- **Bonus diversité** : Encourage la variété dans les recommandations pour éviter la monotonie

### Gestion du cold start (utilisateurs nouveaux/inconnus)

Le système gère automatiquement le problème du **cold start** pour les utilisateurs avec un historique insuffisant ou invalide :

#### Détection intelligente du cold start

Le système utilise une **approche en deux étapes** pour détecter le cold start :

1. **Vérification quantitative** : L'utilisateur doit avoir au moins `MIN_USER_INTERACTIONS` interactions (défaut: **5**)
2. **Validation qualitative** : Les `click_article_id` doivent être valides (présents dans les métadonnées)

**Exemples de scénarios** :

| Scénario utilisateur | Interactions totales | Interactions valides | Comportement |
|---------------------|---------------------|---------------------|--------------|
| Utilisateur nouveau | 0 | 0 | ✅ Fallback vers popularité |
| Peu d'historique | 2 | 2 | ✅ Fallback vers popularité (< 5) |
| Historique suffisant | 10 | 10 | ✅ Recommandations personnalisées |
| Données corrompues | 10 | 0 | ✅ Fallback vers popularité (IDs invalides) |
| Historique partiel | 6 | 3 | ✅ Fallback vers popularité (3 valides < 5) |

**Comportement par méthode** :

| Méthode | Comportement pour historique insuffisant |
|---------|------------------------------------------|
| **Popularité** | ✅ Fonctionne directement (ne dépend pas de l'utilisateur) |
| **Similarité de contenu** | ✅ Fallback automatique sur Popularité si < 5 interactions valides |
| **Clustering** | ✅ Fallback automatique sur Popularité si < 5 interactions valides |
| **Hybride** | ✅ Fallback automatique sur Popularité si < 5 interactions valides |

**Avantages de cette approche** :
- ✅ **Robustesse** : Gère les données corrompues ou invalides
- ✅ **Qualité** : Évite les recommandations basées sur trop peu de données
- ✅ **Aucune erreur** : Fallback automatique au lieu de retourner des listes vides
- ✅ **Recommandations cohérentes** basées sur les tendances actuelles
- ✅ **Logs explicites** : Indique le nombre d'interactions valides et le seuil minimum
- ✅ **Configurable** : Ajustez `MIN_USER_INTERACTIONS` dans `config.py` (valeurs recommandées : 3-10)

**Exemple** : Si un utilisateur a 3 interactions dont seulement 2 sont valides, le système appliquera automatiquement un fallback vers la méthode popularité, car 2 < 5 (seuil minimum).

#### Transparence du fallback dans les réponses API

Lorsqu'un fallback est appliqué, l'API indique clairement cette information **à la fois au niveau racine ET dans les métadonnées** de la réponse :

```json
{
  "user_id": 999999,
  "method": "content",
  "actual_method": "popularity",
  "fallback_applied": true,
  "recommendations": [
    {
      "article_id": 160974,
      "score": 25046.71428571429,
      "reason": "Article populaire (#1) - 34145 utilisateurs, 37213 clics",
      "metadata": {...},
      "fallback_from": "content",
      "fallback_reason": "insufficient_valid_history"
    }
  ],
  "metadata": {
    "requested_method": "content",
    "actual_method": "popularity",
    "fallback_applied": true,
    "fallback_reason": "Cold start: utilisateur avec moins de 5 interactions valides (0 détectées), fallback de 'content' vers 'popularity'",
    "user_stats": {
      "user_id": 999999,
      "total_interactions": 0,
      "unique_articles": 0,
      "date_range": {
        "first_interaction": null,
        "last_interaction": null
      },
      "top_categories": [],
      "is_new_user": true
    }
  },
  "generated_at": "2025-09-30T09:49:40.605752"
}
```

**Champs ajoutés au niveau racine (accès rapide)** :
- `actual_method` : La méthode réellement utilisée après fallback
- `fallback_applied` : Boolean indiquant si un fallback a été effectué

**Champs ajoutés dans les métadonnées (détails)** :
- `requested_method` : La méthode initialement demandée par l'utilisateur
- `actual_method` : La méthode réellement utilisée (identique si pas de fallback)
- `fallback_applied` : Boolean indiquant si un fallback a été effectué
- `fallback_reason` : Explication détaillée du pourquoi du fallback, incluant le nombre d'interactions valides détectées et le seuil minimum requis (uniquement si fallback appliqué)

**Champs ajoutés dans chaque recommandation** :
- `fallback_from` : Indique la méthode d'origine qui a déclenché le fallback
- `fallback_reason` : Code court identifiant la raison (`insufficient_valid_history`)

**Exemple sans fallback (utilisateur existant)** :
```json
{
  "user_id": 5890,
  "method": "content",
  "actual_method": "content",
  "fallback_applied": false,
  "recommendations": [
    {
      "article_id": 208436,
      "score": 0.8247120976448059,
      "reason": "Similaire à vos lectures (score: 0.825)",
      "metadata": {...}
    }
  ],
  "metadata": {
    "requested_method": "content",
    "actual_method": "content",
    "fallback_applied": false,
    "user_stats": {...}
  }
}
```

**Avantages de cette structure** :
- ✅ **Accès facile** : `fallback_applied` et `actual_method` directement au niveau racine
- ✅ **Détection automatique** : Les applications clientes peuvent vérifier le fallback sans parser les métadonnées
- ✅ **Transparence complète** : Toutes les informations nécessaires sont disponibles
- ✅ **Compatibilité** : Les métadonnées conservent aussi ces informations pour les usages avancés
- ✅ **Logging/Analytics** : Facilite le suivi des taux de fallback et la compréhension du comportement utilisateur

**Utilisation côté client** :
```javascript
// Vérification simple
if (response.fallback_applied) {
  console.log(`Fallback détecté: ${response.method} → ${response.actual_method}`);
  showMessage("Recommandations basées sur les tendances actuelles");
}

// Accès direct à la méthode réelle
const effectiveMethod = response.actual_method;
```

### Gestion adaptative des données

- **Détection automatique** de la date de référence (dernier clic enregistré: 2017-11-13 pour ce dataset)
- **Filtrage qualité** : Exclusion des articles < 50 mots et > 2 ans
- **Optimisation temporelle** : Simulation de recommandations en temps réel basée sur les données historiques
- **Cache intelligent** : Mise en cache des calculs coûteux (clusters, popularité)

#### Dates de référence et cohérence temporelle

Le système utilise deux dates de référence distinctes provenant de sources différentes :

- **`reference_date`** : **2017-11-13** (dernier clic enregistré)
  - Source : `interactions['click_timestamp'].max()`
  - Représente la dernière interaction utilisateur dans les données de clics
  - Utilisée comme point de référence temporel pour tous les calculs (fenêtres de popularité, filtrage d'articles, etc.)

- **`max_article_date`** : **2018-03-13** (dernier article publié)
  - Source : `articles_metadata['created_at_ts'].max()`
  - Représente l'article le plus récent dans le catalogue
  - Écart de ~4 mois avec `reference_date`

**Explication de l'écart** : Les datasets d'interactions (`clicks/`) et de métadonnées (`articles_metadata.csv`) ont été extraits à des moments différents, ou les articles publiés entre novembre 2017 et mars 2018 n'ont simplement pas reçu de clics dans les données collectées.

**Impact positif** : Le système utilise correctement `reference_date` (dernière interaction) comme point de référence temporel, ce qui garantit que les recommandations sont cohérentes et n'utilisent pas d'articles "du futur" qui n'avaient pas encore de clics au moment de la dernière interaction enregistrée.

### API REST complète

- **Documentation interactive** automatique avec FastAPI (Swagger UI disonible à `/docs`)
- **Gestion d'erreurs** robuste avec codes HTTP appropriés
- **Validation automatique** des paramètres avec Pydantic
- **Support CORS** pour l'intégration frontend
- **Endpoints de debug** pour le monitoring et les tests

## Lancement du backend de l'application

### Prérequis

- Python 3.8+
- Environnement virtuel (recommandé)
- Données dans le dossier `backend/data/`

### Récupération des fichiers volumineux (Git LFS)

Si vous venez de cloner le dépôt, exécutez la commande suivante depuis la racine du dépôt pour télécharger les fichiers volumineux nécessaires (embeddings, clusters, etc.) :

```bash
git lfs pull
```

### Installation des dépendances

```bash
# Se placer dans le dossier backend
cd backend

# Créer un environnement virtuel (optionnel)
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Démarrage de l'API

**Méthode 1 : Script de lancement (recommandé)**
```bash
chmod +x start.sh
./start.sh
```

**Méthode 2 : Uvicorn direct**
```bash
uvicorn main:app --reload
```

**Méthode 3 : Python**
```bash
python3 main.py
```

### Vérification du démarrage

L'API sera accessible sur :
- **URL principale** : http://localhost:8000
- **Documentation** : http://localhost:8000/docs
- **Santé de l'API** : http://localhost:8000/health

## API - Endpoints et utilisation

### Endpoints principaux

#### 🏥 Santé de l'API
```http
GET /health
```
Retourne le statut de l'API et les statistiques des données chargées.

#### 🎯 Recommandations pour un utilisateur
```http
POST /recommend/{user_id}?method=hybrid&n_recommendations=5&exclude_seen=true
```

**Paramètres :**
- `user_id` : ID de l'utilisateur (requis)
- `method` : Méthode de recommandation (défaut: `hybrid`)
  - `popularity`
  - `content`
  - `clustering`
  - `hybrid`
- `n_recommendations` : Nombre de recommandations (1-20, défaut: 5)
- `exclude_seen` : Exclure les articles déjà vus (défaut: true)

**Exemple de réponse :**
```json
{
  "user_id": 12345,
  "method": "hybrid",
  "recommendations": [
    {
      "article_id": 156789,
      "score": 0.847,
      "reason": "Score hybride: 0.847 (clustering: 0.892, content: 0.756)",
      "metadata": {
        "article_id": 156789,
        "category_id": 281,
        "words_count": 195,
        "created_date": "2018-01-15T10:30:00"
      }
    }
  ],
  "metadata": {
    "method": "hybrid",
    "user_stats": {
      "total_interactions": 23,
      "unique_articles": 20
    }
  },
  "generated_at": "2024-01-15T14:30:00"
}
```

#### 👥 Liste des utilisateurs
```http
GET /users?limit=100
```
Retourne la liste des utilisateurs disponibles pour les tests.

#### 📊 Statistiques d'un utilisateur
```http
GET /users/{user_id}/stats
```
Informations détaillées sur l'activité d'un utilisateur.

#### 🏷️ Segment d'un utilisateur
```http
GET /users/{user_id}/segment
```
Retourne le cluster/segment de l'utilisateur et ses caractéristiques.

#### 📄 Informations sur un article
```http
GET /articles/{article_id}
```
Métadonnées complètes d'un article.

#### 🔥 Articles populaires
```http
GET /popular?limit=10
```
Liste des articles les plus populaires récemment.

### Endpoints de debug

#### ⚙️ Configuration actuelle
```http
GET /debug/config
```

#### 📈 Statistiques détaillées des données
```http
GET /debug/data-stats
```

## Tests et validation

### Script de test automatique

```bash
# Lancer les tests complets de l'API
python3 scripts/test_api.py
```

Ce script teste :
- La santé de l'API
- La récupération des utilisateurs
- Les statistiques utilisateur
- Toutes les méthodes de recommandation
- Les articles populaires

### Tests manuels avec curl

```bash
# Test de santé
curl http://localhost:8000/health

# Recommandations hybrides pour un utilisateur
curl -X POST "http://localhost:8000/recommend/5890?method=hybrid&n_recommendations=5"

# Recommandations par similarité de contenu
curl -X POST "http://localhost:8000/recommend/5890?method=content&n_recommendations=5&exclude_seen=true"

# Recommandations par popularité
curl -X POST "http://localhost:8000/recommend/5890?method=popularity&n_recommendations=5"

# Recommandations par clustering
curl -X POST "http://localhost:8000/recommend/5890?method=clustering&n_recommendations=5"

# Informations sur le segment/cluster d'un utilisateur
curl http://localhost:8000/users/5890/segment

# Caractéristiques de tous les segments/clusters d'utilisateurs
curl http://localhost:8000/clusters

# Liste des utilisateurs
curl http://localhost:8000/users?limit=10

# Statistiques d'un utilisateur
curl http://localhost:8000/users/5890/stats

# Articles populaires
curl http://localhost:8000/popular?limit=5

# Statistiques détaillées des données (debug)
curl http://localhost:8000/debug/data-stats
```

### Interface de documentation interactive

Accédez à http://localhost:8000/docs pour :
- Voir tous les endpoints disponibles
- Tester directement l'API depuis le navigateur
- Consulter les schémas de données
- Voir les exemples de requêtes/réponses

## Architecture technique

### Structure du projet

```
backend/
├── main.py                 # Application FastAPI principale
├── config.py              # Configuration et paramètres
├── models.py              # Modèles Pydantic pour l'API
├── data_loader.py         # Gestionnaire centralisé des données
├── recommenders/          # Moteurs de recommandation
│   ├── __init__.py
│   ├── base.py           # Classe de base
│   ├── popularity.py     # Recommandation par popularité
│   ├── content.py        # Recommandation par contenu
│   ├── clustering.py     # Recommandation par clustering
│   └── hybrid.py         # Recommandation hybride
├── data/                 # Données du projet
├── scripts/              # Scripts utilitaires
└── requirements.txt      # Dépendances Python
```

### Technologies utilisées

- **FastAPI** : Framework web moderne et performant
- **Pydantic** : Validation et sérialisation des données
- **Pandas** : Manipulation des données
- **NumPy** : Calculs numériques et embeddings
- **Scikit-learn** : Algorithmes de clustering et similarité
- **Uvicorn** : Serveur ASGI haute performance

### Optimisations implémentées

- **Lazy loading** des recommandeurs (créés à la demande)
- **Cache des embeddings** et métadonnées en mémoire
- **Clustering paresseux** avec mise à jour quotidienne
- **Pré-calcul des articles recommandables** avec filtres qualité
- **Normalisation adaptative** des scores par méthode

## Configuration et personnalisation

### Paramètres principaux (config.py)

```python
MAX_ARTICLE_AGE_DAYS = 730       # Âge maximum des articles (jours)
MIN_WORDS_COUNT = 50             # Nombre minimum de mots par article
N_USER_CLUSTERS = 5              # Nombre de segments utilisateurs
MIN_USER_INTERACTIONS = 5        # Seuil pour cold start (interactions valides requises)
                                 # Valeurs recommandées : 3 (permissif), 5 (équilibré), 10 (conservateur)

# Poids de l'approche hybride
HYBRID_WEIGHTS = {
    "clustering": 0.4,           # Filtrage collaboratif
    "content": 0.3,              # Similarité de contenu
    "popularity": 0.2,           # Popularité normalisée par âge
    "diversity": 0.1             # Bonus diversité
}
```

### Variables d'environnement

Créez un fichier `.env` dans le dossier `backend/` pour personnaliser :

```env
DATA_PATH=data
MAX_ARTICLE_AGE_DAYS=730
MIN_WORDS_COUNT=50
N_RECOMMENDATIONS=5
N_USER_CLUSTERS=5
```

## Monitoring et logs

### Logs de l'application

L'API génère des logs détaillés :
- **INFO** : Démarrage, chargement des données, recommandations générées
- **WARNING** : Fallbacks, données manquantes
- **ERROR** : Erreurs de traitement, exceptions

### Métriques disponibles

Via `/debug/data-stats` :
- Nombre total d'articles et utilisateurs
- Statistiques des interactions
- Performance des recommandeurs
- État des clusters utilisateurs

---

## Scénario de production : Ajout dynamique d'utilisateurs et d'articles

### Vue d'ensemble

L'application actuelle s'appuie sur des données statiques (fichiers CSV et pickle) qui représentent une **base de données figée** avec trois tables principales :
- **`clicks`** : Interactions utilisateur-article (322K utilisateurs, 2.9M clics)
- **`articles`** : Métadonnées des articles avec embeddings pré-calculés (364K articles)
- **`users`** : Dérivée implicitement des interactions

Dans un **scénario de production avec une vraie base de données**, voici ce qui se passerait lors de l'ajout de nouveaux utilisateurs et/ou articles.

### 🆕 Ajout de nouveaux utilisateurs

#### Comportement actuel : ✅ **Géré automatiquement**

L'application gère très bien l'ajout de nouveaux utilisateurs grâce au **système de cold start** :

**Phase 1 : Nouvel utilisateur sans historique**
```
Utilisateur 999999 (nouveau)
→ Méthode "Similarité de contenu" : ✅ Fallback automatique sur "popularité"
→ Méthode "Clustering" : ✅ Fallback automatique sur "popularité"
→ Méthode "Hybride" : ✅ Combine les fallbacks (popularité prédominante)
→ Résultat : Recommandations basées sur les tendances actuelles
```

**Phase 2 : Premières interactions (1-4 clics valides)**
```
Utilisateur 999999 (3 clics valides)
→ Méthode "Similarité de contenu" : ✅ Fallback sur popularité (< 5 interactions requises)
→ Méthode "Clustering" : ✅ Fallback sur popularité (< 5 interactions requises)
→ Méthode "Hybride" : ✅ Fallback sur popularité
→ Résultat : Recommandations basées sur les tendances actuelles
```

**Phase 3 : Utilisateur actif (≥5 interactions valides)**
```
Utilisateur 999999 (15 clics valides)
→ Méthode "Similarité de contenu" : ✅ Profil utilisateur riche (moyenne des embeddings consultés)
→ Méthode "Clustering" : ✅ Assigné à un cluster (après recalcul quotidien)
→ Méthode "Hybride" : ✅ Combinaison des 3 méthodes avec pondération
→ Résultat : Recommandations personnalisées complètes
```

**Note importante** : Le système valide automatiquement les `click_article_id` pour s'assurer qu'ils existent dans les métadonnées. Seules les interactions valides sont comptabilisées pour déterminer le seuil de cold start.

#### Architecture en production

**Avec une base de données SQL/NoSQL** :
1. **Insertion en temps réel** : Chaque clic → `INSERT INTO clicks (user_id, article_id, timestamp)`
2. **Profil utilisateur dynamique** : Recalculé à chaque requête à partir de l'historique récent
3. **Mise à jour des clusters** :
   - **Option A (batch)** : Recalcul quotidien des clusters (config actuelle : 24h)
   - **Option B (streaming)** : Assignation dynamique des nouveaux utilisateurs au cluster le plus proche
   - **Option C (hybride)** : Assignation temporaire + réassignation lors du batch quotidien

**Exemple de requête SQL pour le profil utilisateur** :
```sql
-- Récupérer les 10 derniers articles consultés
SELECT article_id
FROM clicks
WHERE user_id = 999999
ORDER BY timestamp DESC
LIMIT 10;

-- Calculer le profil utilisateur (moyenne des embeddings)
-- → Effectué en Python après récupération des embeddings
```

**Impact sur les performances** :
- ✅ **Faible** : Les nouveaux utilisateurs n'affectent pas les performances globales
- ⚠️ **Recalcul des clusters** : Coût computationnel proportionnel au nombre total d'utilisateurs
  - Actuel : ~322K utilisateurs → ~30s de calcul
  - Production (1M utilisateurs) → Envisager un clustering incrémental ou un échantillonnage

### 📄 Ajout de nouveaux articles

#### Comportement actuel : ⚠️ **Limitations majeures**

L'ajout de nouveaux articles pose des **défis critiques** en raison des embeddings statiques :

**Problème 1 : Embeddings manquants**
```
Nouvel article ID 400000 (publié aujourd'hui)
→ Métadonnées : ✅ Chargées depuis articles_metadata.csv
→ Embeddings : ❌ Absents (fichier articles_embeddings.pickle figé)
→ Conséquence :
   - Méthode "Similarité de contenu" : ❌ L'article ne peut PAS être recommandé (embeddings requis)
   - Méthode "Popularité" : ✅ Fonctionne (ne dépend pas des embeddings)
   - Méthode "Clustering" : ✅ Fonctionne (popularité dans les clusters, pas d'embeddings requis)
```

**Problème 2 : Cold start des articles sans interactions**
- Un nouvel article sans aucun clic aura un score de popularité nul (0 clics / âge)
- Risque : Article peu visible tant qu'il n'a pas reçu ses premières interactions
- ⚠️ **Important** : Contrairement aux méthodes basées sur les embeddings, la méthode "Popularité" peut théoriquement recommander l'article dès qu'il reçoit son premier clic (le score devient > 0)
- Pour les articles très récents avec quelques clics, la normalisation par âge leur donne un avantage (ex: 10 clics en 1 jour vs 100 clics en 30 jours)

**Problème 3 : Désynchronisation des données**
- Les embeddings sont indexés par `article_id` (0 à 363,046)
- Un nouvel article ID 400000 est **hors des limites du tableau NumPy**
- Risque : `IndexError` ou résultats corrompus

#### Architecture recommandée en production

Pour gérer efficacement l'ajout d'articles, plusieurs adaptations sont nécessaires :

##### 1. Pipeline de génération d'embeddings en temps réel

**Option A : Génération à la publication**
```python
# Lors de l'ajout d'un nouvel article dans la BDD
new_article = {
    "article_id": 400000,
    "content": "Texte de l'article...",
    "category_id": 281,
    "words_count": 250
}

# Générer l'embedding immédiatement
embedding = generate_embedding(new_article["content"])  # Modèle pré-entraîné

# Insérer dans la BDD
db.execute("""
    INSERT INTO articles (article_id, category_id, words_count, embedding)
    VALUES (%s, %s, %s, %s)
""", (new_article["article_id"], new_article["category_id"],
      new_article["words_count"], embedding.tobytes()))
```

**Option B : Génération en batch différé**
```python
# Toutes les heures, traiter les articles sans embeddings
pending_articles = db.execute("""
    SELECT article_id, content
    FROM articles
    WHERE embedding IS NULL
""")

for article in pending_articles:
    embedding = generate_embedding(article["content"])
    db.execute("""
        UPDATE articles
        SET embedding = %s
        WHERE article_id = %s
    """, (embedding.tobytes(), article["article_id"]))
```

**Technologies recommandées** :
- **Modèle d'embeddings** : Sentence-BERT (multilingual), USE (Universal Sentence Encoder)
- **Infrastructure** :
  - API de génération (FastAPI + GPU)
  - Queue de traitement (Celery + Redis)
  - Cache des embeddings (Redis ou Memcached)

##### 2. Stratégie de cold start pour nouveaux articles

**Solution 1 : Boost temporaire de nouveauté**
```python
# Ajouter un bonus de popularité pour les nouveaux articles
article_age_hours = (now - article.created_at).total_seconds() / 3600

if article_age_hours < 24:  # Moins de 24h
    novelty_boost = 1.5  # +50% de score
elif article_age_hours < 72:  # 1-3 jours
    novelty_boost = 1.2  # +20% de score
else:
    novelty_boost = 1.0  # Pas de bonus

final_score = popularity_score * novelty_boost
```

**Solution 2 : Recommandations "Articles récents" dédiées**
```python
# Endpoint spécifique pour les nouveautés
@app.get("/articles/recent")
def get_recent_articles(category: Optional[int] = None):
    """Retourne les articles publiés dans les dernières 48h"""
    cutoff = datetime.now() - timedelta(hours=48)
    recent = db.query(Article).filter(Article.created_at >= cutoff)
    if category:
        recent = recent.filter(Article.category_id == category)
    return recent.order_by(Article.created_at.desc()).limit(10)
```

**Solution 3 : Recommandations par similarité de métadonnées**
```python
# Si embedding manquant, utiliser les métadonnées (catégorie, mots-clés)
def recommend_without_embedding(user_id, new_article_id):
    # Récupérer les catégories préférées de l'utilisateur
    user_top_categories = get_user_top_categories(user_id)

    # Recommander le nouvel article si dans ces catégories
    new_article = get_article(new_article_id)
    if new_article.category_id in user_top_categories:
        return True  # Recommander
    return False
```

##### 3. Gestion de la cohérence des données

**Architecture base de données recommandée** :

```sql
-- Table articles avec embeddings
CREATE TABLE articles (
    article_id BIGINT PRIMARY KEY,
    category_id INT NOT NULL,
    publisher_id INT,
    words_count INT,
    created_at TIMESTAMP NOT NULL,
    embedding VECTOR(250),  -- Type natif PostgreSQL avec pgvector
    INDEX idx_category (category_id),
    INDEX idx_created_at (created_at)
);

-- Table clicks (interactions)
CREATE TABLE clicks (
    click_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    article_id BIGINT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user (user_id),
    INDEX idx_article (article_id),
    INDEX idx_timestamp (timestamp),
    FOREIGN KEY (article_id) REFERENCES articles(article_id)
);

-- Table user_clusters (mise à jour quotidienne)
CREATE TABLE user_clusters (
    user_id BIGINT PRIMARY KEY,
    cluster_id INT NOT NULL,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cluster (cluster_id)
);

-- Vue matérialisée pour la popularité (rafraîchie toutes les heures)
CREATE MATERIALIZED VIEW article_popularity AS
SELECT
    article_id,
    COUNT(DISTINCT user_id) AS unique_users,
    COUNT(*) AS total_clicks,
    MAX(timestamp) AS last_interaction
FROM clicks
WHERE timestamp >= NOW() - INTERVAL '7 days'
GROUP BY article_id;
```

**Avantages de PostgreSQL + pgvector** :
- ✅ Stockage natif des embeddings (type `VECTOR`)
- ✅ Recherche de similarité en SQL : `ORDER BY embedding <-> query_embedding LIMIT 10`
- ✅ Index HNSW pour recherche approximative rapide (millions d'articles)
- ✅ Transactions ACID pour cohérence des données

##### 4. Mise à jour incrémentale des recommandeurs

**Clustering : Stratégie hybride**
```python
class IncrementalClusteringRecommender:
    def assign_new_user_to_cluster(self, user_id: int) -> int:
        """Assigne un nouvel utilisateur au cluster le plus proche"""
        # Construire les features du nouvel utilisateur
        user_features = self._build_user_features([user_id])
        user_features_scaled = self._scaler.transform(user_features)

        # Prédire le cluster (pas de réentraînement)
        cluster = self._cluster_model.predict(user_features_scaled)[0]

        # Sauvegarder l'assignation temporaire
        db.execute("""
            INSERT INTO user_clusters (user_id, cluster_id, temporary)
            VALUES (%s, %s, TRUE)
        """, (user_id, cluster))

        return cluster

    def retrain_clusters_batch(self):
        """Réentraînement complet des clusters (quotidien)"""
        # Marquer toutes les assignations comme définitives
        self._train_clusters()  # Méthode actuelle

        db.execute("""
            UPDATE user_clusters SET temporary = FALSE
        """)
```

**Content-based : Rechargement dynamique**
```python
class DynamicContentRecommender:
    def load_article_embedding(self, article_id: int) -> np.ndarray:
        """Charge l'embedding d'un article depuis la BDD"""
        # Cache en mémoire (LRU)
        if article_id in self._embedding_cache:
            return self._embedding_cache[article_id]

        # Requête BDD
        result = db.execute("""
            SELECT embedding FROM articles WHERE article_id = %s
        """, (article_id,))

        if result:
            embedding = np.frombuffer(result[0], dtype=np.float32)
            self._embedding_cache[article_id] = embedding
            return embedding
        else:
            raise ValueError(f"Embedding manquant pour article {article_id}")
```

### 📊 Tableau récapitulatif : Ajout d'utilisateurs vs. Articles

| Aspect | **Nouvel utilisateur** | **Nouvel article** |
|--------|------------------------|---------------------|
| **Gestion actuelle** | ✅ Excellente (cold start) | ❌ Problématique (embeddings statiques) |
| **Délai avant recommandations** | ✅ Immédiat (fallback popularité) | ⚠️ Après premières interactions + embedding généré |
| **Impact sur "Clustering"** | ⚠️ Assignation différée (24h) | ➖ Aucun (clusters basés sur utilisateurs) |
| **Impact sur "Similarité de contenu"** | ✅ Profil dès 1ère interaction | ❌ Impossible sans embedding |
| **Impact sur "Popularité"** | ✅ Fonctionne immédiatement | ⚠️ Score nul jusqu'à premières interactions |
| **Coût computationnel** | ⚠️ Moyen (recalcul clusters quotidien) | 🔥 Élevé (génération embeddings) |
| **Adaptation BDD requise** | ✅ Minime (INSERT dans clicks) | 🔥 Majeure (pipeline embeddings) |

### 🚀 Recommandations pour la mise en production

#### Phase 1 : Migration vers une base de données
1. **PostgreSQL + pgvector** pour le stockage des embeddings
2. **Vues matérialisées** pour les calculs de popularité (rafraîchies toutes les heures)
3. **Index optimisés** sur `user_id`, `article_id`, `timestamp`

#### Phase 2 : Pipeline d'embeddings
1. **Service de génération** : API dédiée avec GPU (FastAPI + Sentence-BERT)
2. **Queue de traitement** : Celery + Redis pour traiter les nouveaux articles en asynchrone
3. **Fallback temporaire** : Recommandations par métadonnées en attendant l'embedding

#### Phase 3 : Optimisation des clusters
1. **Clustering incrémental** : Assignation immédiate des nouveaux utilisateurs
2. **Réentraînement adaptatif** : Quotidien si < 100K users, hebdomadaire au-delà
3. **Monitoring** : Tracker la stabilité des clusters (taux de réassignation)

#### Phase 4 : Gestion du cold start des articles
1. **Boost de nouveauté** : Bonus temporaire pour articles récents (24-72h)
2. **Section dédiée** : "Nouveaux articles" dans l'interface utilisateur
3. **A/B testing** : Tester différentes stratégies de promotion des nouveaux contenus
