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

### Analyse des interactions utilisateurs

```bash
# Compter les utilisateurs et analyser les interactions
python3 backend/scripts/count_users.py
```

**Résultats clés :**
- 👥 **322,897 utilisateurs uniques**
- 📄 **46,033 articles consultés** (sur 364K disponibles)
- 🖱️ **2,988,181 clics** au total
- 📊 **9.3 clics/utilisateur** en moyenne
- 📊 **64.9 clics/article** en moyenne
- 📁 **385 fichiers horaires** de données

### Analyse des métadonnées des articles

```bash
# Analyser les caractéristiques des articles
python3 backend/scripts/analyze_articles_metadata.py
```

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
- **Articles très courts** : 3,729 articles < 50 mots (à filtrer ?)

### 🎯 **Adaptations pour nos recommandeurs**

#### **1. Popularité récente**
- ✅ Fenêtre de 3 jours sera parfaite
- ✅ Focus sur 2017-2018 (données les plus denses)

#### **2. Content-based**  
- ✅ 461 catégories = excellent pour la diversification
- ✅ Embeddings sur 364K articles = très riche
- ⚠️ Filtrer les articles < 50 mots

#### **3. Clustering utilisateurs**
- ✅ 461 catégories = bonnes features pour segmenter
- ✅ 5 clusters seront suffisants avec cette distribution

#### **4. Hybride**
- ✅ Équilibrage 40/30/20/10 adapté à cette diversité

---

# Backend FastAPI

## Fonctionnalités implémentées

### Système de recommandation multi-approches

L'application implémente **4 méthodes de recommandation** complémentaires :

- **🔥 Popularité récente** : Recommande les articles les plus consultés dans les 90 derniers jours
- **📖 Similarité de contenu** : Utilise les embeddings pour recommander des articles similaires à ceux déjà lus
- **👥 Clustering d'utilisateurs** : Segmente les utilisateurs en 5 groupes et recommande les articles populaires dans chaque segment  
- **🎭 Hybride** : Combine intelligemment les 3 approches précédentes avec pondération (40% clustering, 30% contenu, 20% popularité, 10% diversité)

### Gestion adaptative des données

- **Détection automatique** de la date de référence (mars 2018 pour ce dataset)
- **Filtrage qualité** : Exclusion des articles < 50 mots et > 2 ans
- **Optimisation temporelle** : Simulation de recommandations en temps réel basée sur les données historiques
- **Cache intelligent** : Mise en cache des calculs coûteux (clusters, popularité)

### API REST complète

- **Documentation interactive** automatique avec FastAPI
- **Gestion d'erreurs** robuste avec codes HTTP appropriés
- **Validation automatique** des paramètres avec Pydantic
- **Support CORS** pour l'intégration frontend
- **Endpoints de debug** pour le monitoring et les tests

## Lancement du backend de l'application

### Prérequis

- Python 3.8+
- Environnement virtuel (recommandé)
- Données dans le dossier `backend/data/`

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
curl -X POST "http://localhost:8000/recommend/12345?method=hybrid&n_recommendations=5"

# Liste des utilisateurs
curl http://localhost:8000/users?limit=10
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
POPULARITY_WINDOW_DAYS = 90      # Fenêtre de popularité (jours)
MAX_ARTICLE_AGE_DAYS = 730       # Âge maximum des articles (jours)
MIN_WORDS_COUNT = 50             # Nombre minimum de mots par article
N_USER_CLUSTERS = 5              # Nombre de segments utilisateurs
MIN_USER_INTERACTIONS = 3         # Seuil pour "nouveaux utilisateurs"

# Poids de l'approche hybride
HYBRID_WEIGHTS = {
    "clustering": 0.4,           # Filtrage collaboratif
    "content": 0.3,              # Similarité de contenu
    "popularity": 0.2,           # Popularité récente
    "diversity": 0.1             # Bonus diversité
}
```

### Variables d'environnement

Créez un fichier `.env` dans le dossier `backend/` pour personnaliser :

```env
DATA_PATH=data
POPULARITY_WINDOW_DAYS=90
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

## Déploiement en production

### Préparation

1. **Configurer les variables d'environnement**
2. **Utiliser Gunicorn** pour la production :
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Ajouter un reverse proxy** (nginx) pour les performances
4. **Configurer CORS** selon vos domaines frontend

### Docker (optionnel)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```