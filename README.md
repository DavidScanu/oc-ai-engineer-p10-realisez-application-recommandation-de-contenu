# Projet 10 : Réalisez une application de recommandation de contenu

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Node.js](https://img.shields.io/badge/Node.js-20%2B-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14%2B-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![Azure](https://img.shields.io/badge/Azure-Functions-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![Dataset](https://img.shields.io/badge/Dataset-Globo.com-red)](https://www.kaggle.com/gspmoreira/news-portal-user-interactions-by-globocom)

> 🎓 OpenClassrooms • Parcours [AI Engineer](https://openclassrooms.com/fr/paths/795-ai-engineer) | 👋 *Étudiant* : [David Scanu](https://www.linkedin.com/in/davidscanu14/)

## 🎯 Contexte

My Content est une start-up innovante qui souhaite encourager la lecture en recommandant des contenus pertinents et personnalisés à ses utilisateurs. Dans un premier temps, nous nous concentrons sur la **recommandation d'articles et de livres aux particuliers**.

En tant que CTO et cofondateur aux côtés de Samia (CEO), nous sommes en pleine construction d'un premier MVP (Minimum Viable Product) sous forme d'application. Comme nous ne disposons pas encore de données utilisateurs propres, nous utilisons un dataset public de haute qualité : [les interactions des utilisateurs du portail d'actualités brésilien Globo.com](https://www.kaggle.com/gspmoreira/news-portal-user-interactions-by-globocom#clicks_sample.csv) (3 millions de clics, 322K utilisateurs, 46K articles).

Cette approche nous permet de **développer et valider notre système de recommandation** avant le lancement commercial, tout en nous assurant de la scalabilité de notre architecture technique pour gérer **l'ajout futur de nouveaux utilisateurs et articles**.

## 🚀 Mission

Notre mission se décline en trois axes principaux :

### 1. Backend : Développement du système de recommandation
Nous devons créer un système de recommandation multi-approches capable de :
- Suggérer 5 articles pertinents à chaque utilisateur
- Gérer le cold start (nouveaux utilisateurs et nouveaux articles)
- Combiner plusieurs méthodes : popularité, similarité de contenu, clustering utilisateurs, et approche hybride

### 2. Architecture serverless avec Azure Functions
Nous mettons en place une architecture cloud scalable qui :
- Expose le système de recommandation via Azure Functions
- Permet un déploiement rapide et économique
- Supporte une montée en charge progressive

### 3. Frontend : Application de démonstration
Nous développons une interface simple qui :
- Liste les utilisateurs disponibles
- Affiche les 5 recommandations d'articles pour l'utilisateur sélectionné
- Démontre les fonctionnalités à Samia et aux futurs utilisateurs

## 📦 Livrables et démonstration

### 📱 Application de démonstration
- Frontend : Interface utilisateur simple
  - URL de production : (à venir)
- Backend : Système de recommandation serverless déployé sur Azure Functions
  - URL de production : (à venir)
- Entrée : ID utilisateur → Sortie : Top 5 articles recommandés
- Démonstration des fonctionnalités complètes du système

### 💻 [Code source versionné](https://github.com/DavidScanu/oc-ai-engineer-p10-realisez-application-recommandation-de-contenu)
- Dépôt GitHub avec architecture complète
- Scripts de prétraitement des données
- Modèles de recommandation (4 approches)
- Configuration Azure Functions
- Documentation technique (README détaillé)
- Code permettant un déploiement end-to-end

### 📊 [Support de présentation]()
- Document PowerPoint/PDF (15-25 slides)
- Description fonctionnelle de l'application
- Analyse comparative des modèles testés (avantages/inconvénients)
- Schéma de l'architecture technique retenue
- Présentation détaillée du système de recommandation
- Schéma de l'architecture cible évolutive (gestion nouveaux users/articles)

## 📋 Plan d'action

### Phase 1 : Exploration et compréhension (✅ Complété)
- [x] Analyse exploratoire du dataset Globo.com
- [x] Compréhension des défis du cold start
- [x] Identification des features pertinentes

### Phase 2 : Développement des recommandeurs (✅ Complété)
- [x] Implémentation de la méthode **Popularité** (normalisée par âge)
- [x] Développement de la **Similarité de contenu** (embeddings)
- [x] Création du **Clustering utilisateurs** (5 segments)
- [x] Conception de l'approche **Hybride** (combinaison pondérée)

### Phase 3 : Architecture backend (✅ Complété)
- [x] API FastAPI avec endpoints REST complets
- [x] Système de fallback automatique pour cold start
- [x] Gestion adaptative des dates de référence
- [x] Cache intelligent des calculs coûteux
- [x] Documentation interactive (Swagger)

### Phase 4 : Déploiement Azure (En cours)
- [ ] Configuration Azure Functions (Consumption Plan)
- [ ] Déploiement des modèles et embeddings
- [ ] Tests de performance et monitoring
- [ ] Optimisation des coûts (gestion des services gratuits)

### Phase 5 : Application frontend (À venir)
- [ ] Interface de sélection des utilisateurs
- [ ] Affichage des recommandations avec métadonnées
- [ ] Intégration avec Azure Functions
- [ ] Tests utilisateurs avec Samia

### Phase 6 : Documentation et présentation (À venir)
- [ ] Finalisation du README technique
- [ ] Création du support de présentation
- [ ] Préparation de la démonstration live
- [ ] Documentation de l'architecture cible


## 📊 Analyse exploratoire des données

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

## ✨ Fonctionnalités implémentées

### Système de recommandation multi-approches

L'application implémente **4 méthodes de recommandation** complémentaires :

- **🔥 Popularité normalisée par âge** : Recommande les articles avec le meilleur ratio clics/mois d'existence (favorise les tendances récentes)
- **📖 Similarité de contenu** : Utilise les embeddings pour recommander des articles similaires à ceux déjà lus
- **👥 Clustering d'utilisateurs** : Segmente les utilisateurs en 5 groupes et recommande les articles populaires dans chaque segment
- **🎭 Hybride** : Combine intelligemment les 3 approches précédentes avec pondération (40% clustering, 30% contenu, 20% popularité, 10% diversité)

### 🔥 Méthode 1 : Popularité normalisée par âge (avec boost de nouveauté)

**Principe** : Recommande les articles avec le meilleur ratio clics/mois d'existence, favorisant les tendances récentes. Pour les nouveaux articles, un boost temporaire est appliqué pour compenser le manque de clics initiaux.

**Formule de base** :
```python
# Étape 1 : Score de popularité brut normalisé par l'âge
raw_score = (0.7 × unique_users + 0.3 × total_clicks)
popularity_score = raw_score / article_age_months

# Étape 2 : Boost temporaire de nouveauté (pour les nouveaux aerticles)
if article_age_hours < 24:
    final_score = popularity_score × 1.5  # +50% pour articles < 24h
elif article_age_hours < 72:
    final_score = popularity_score × 1.2  # +20% pour articles 24-72h
else:
    final_score = popularity_score       # Pas de boost après 3 jours
```

**Exemple concret** :
```
Article A (ancien, 8 mois) : 800 clics → score = 800/8 = 100 clics/mois
Article B (récent, 1 jour)  : 10 clics → score = (10/0.03) × 1.5 = 500 clics/mois équivalents
→ Article B bénéficie du boost nouveauté et devient plus visible malgré moins de clics
```

**Avantages** :
- ✅ **Équité temporelle** : Les nouveaux articles ne sont pas désavantagés
- ✅ **Détection de tendances** : Favorise les articles récents avec bon engagement
- ✅ **Cold start résolu** : Boost automatique pour nouveaux articles
- ✅ **Dégradé progressif** : Le boost diminue naturellement avec le temps

**Gestion du cold start** :
- ✅ **Nouveaux utilisateurs** : Fonctionne directement (pas d'historique requis)
- ✅ **Nouveaux articles** : Boost ×1.5 si < 24h compense le faible nombre de clics initial

**Configuration** : Ajustez `NOVELTY_BOOST_24H` et `NOVELTY_BOOST_72H` dans [config.py](backend/config.py)

---

### 📖 Méthode 2 : Similarité de contenu (embeddings + fallback métadonnées)

**Principe** : Recommande des articles similaires à ceux déjà consultés par l'utilisateur, basé sur leurs représentations vectorielles.

**Architecture** :
```python
# Approche principale : Embeddings
user_profile = mean(embeddings_of_read_articles)  # Vecteur 250D
similarities = cosine_similarity(user_profile, all_article_embeddings)
recommendations = top_N(similarities)

# ✅ Fallback métadonnées (Solution 3 implémentée)
if embedding_missing or insufficient_history:
    user_top_categories = get_user_top_categories(user_id, top_n=3)
    avg_words = get_user_avg_words_preference(user_id)

    # Scorer par similarité de catégories et longueur d'articles
    candidates = articles[articles.category_id.isin(user_top_categories)]
    candidates['score'] = 1.0 / (1.0 + abs(words_count - avg_words) / avg_words)

    # Bonus pour catégories favorites (top 1: +0.3, top 2: +0.2, top 3: +0.1)
    recommendations = top_N(candidates.sort_values('score'))
```

**Caractéristiques** :
- **Embeddings pré-calculés** : Vecteurs de 250 dimensions (Sentence-BERT)
- **Mesure de similarité** : Cosine similarity pour trouver les articles les plus proches
- **Profil utilisateur dynamique** : Moyenne des embeddings des articles lus
- **Filtrage qualité** : Exclusion des articles < 50 mots ou > 2 ans

**Gestion du cold start** :
- ✅ **Nouveaux utilisateurs** : Fallback automatique vers popularité si < 5 articles uniques lus
- ✅ **Nouveaux articles sans embeddings** : Fallback utilisant les métadonnées pour la recommandation : 
  - Utilise les **catégories préférées de l'utilisateur**
  - Compare la **longueur d'articles** (`words_count`)
  - **Scoring par similarité de métadonnées**

**Avantages du fallback métadonnées** :
- ✅ **Personnalisé** : Basé sur les préférences réelles de l'utilisateur
- ✅ **Léger** : Pas de calcul d'embeddings coûteux
- ✅ **Robuste** : Fonctionne même avec embeddings manquants

---

### 👥 Méthode 3 : Clustering d'utilisateurs (filtrage collaboratif)

**Principe** : Regroupe les utilisateurs ayant des comportements similaires et recommande les articles populaires dans chaque segment.

**Architecture** :
```python
# Étape 1 : Construction des features utilisateurs
user_features = [
    total_clicks, unique_articles, category_diversity,
    avg_words_preference, clicks_per_hour,
    top_10_categories_preferences  # Ratio de clics par catégorie
]

# Étape 2 : Clustering K-means (5 segments)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(user_features)
clusters = KMeans(n_clusters=5).fit_predict(features_scaled)

# Étape 3 : Recommandations par cluster
cluster_id = get_user_cluster(user_id)
cluster_users = users[users.cluster == cluster_id]
popular_in_cluster = get_popular_articles_for_users(cluster_users)
```

**Caractéristiques des segments** :
- **5 clusters** basés sur le comportement de lecture (activité, diversité, préférences)
- **Mise à jour quotidienne** : Recalcul automatique toutes les 24h
- **Assignation intelligente** : Nouveaux utilisateurs assignés après suffisamment d'interactions
- **Cache persistant** : Sauvegarde sur disque pour démarrage rapide

**Gestion du cold start** :
- ✅ **Nouveaux utilisateurs** : Fallback automatique vers popularité si < 5 articles uniques lus
- ✅ **Assignation différée** : Clustering après accumulation d'un historique suffisant
- ⚠️ **Nouveaux articles** : Pas d'impact (clusters basés sur utilisateurs, pas articles)

**Avantages** :
- ✅ **Découverte** : Recommande des articles appréciés par des utilisateurs similaires
- ✅ **Diversité** : Introduit des articles hors du profil habituel de l'utilisateur
- ✅ **Scalabilité** : Calcul en batch, performances optimales

**Configuration** : Ajustez `N_USER_CLUSTERS` et `CLUSTER_UPDATE_FREQUENCY_HOURS` dans [config.py](backend/config.py)

---

### 🎭 Méthode 4 : Approche hybride (combinaison intelligente)

**Principe** : Combine les 3 méthodes précédentes avec pondération optimisée pour maximiser pertinence et diversité.

**Architecture** :
```python
# Collecte des recommandations de chaque méthode
clustering_recs = clustering.recommend(user_id, n=10)    # Filtrage collaboratif
content_recs = content.recommend(user_id, n=10)         # Similarité de contenu
popularity_recs = popularity.recommend(user_id, n=10)   # Popularité normalisée

# Agrégation avec pondération
for article_id in all_recommendations:
    score = (
        0.4 × normalize(clustering_score) +      # 40% filtrage collaboratif
        0.3 × normalize(content_score) +         # 30% similarité contenu
        0.2 × normalize(popularity_score) +      # 20% tendances actuelles
        0.1 × diversity_bonus                    # 10% bonus diversité
    )

    # Bonus consensus si l'article apparaît dans plusieurs méthodes
    if appears_in_multiple_methods:
        score += 0.1 × (methods_count - 1)

recommendations = top_N(sorted_by_score)
```

**Pondérations par défaut** :
- **40% Clustering** : Filtrage collaboratif (découverte)
- **30% Contenu** : Similarité de contenu (pertinence)
- **20% Popularité** : Tendances actuelles (fraîcheur)
- **10% Diversité** : Bonus pour nouvelles catégories (exploration)

**Normalisation des scores** :
- Clustering : `score / 10.0` (scores souvent > 1)
- Contenu : `score` (déjà entre 0 et 1)
- Popularité : `score / 100.0` (scores peuvent être élevés)

**Gestion du cold start** :
- ✅ **Nouveaux utilisateurs** : Fallback automatique vers popularité (avec boost nouveauté)
- ✅ **Nouveaux articles** : Bénéficient du boost ×1.5 via la composante popularité (20%)
- ✅ **Approche gracieuse** : Combine les méthodes disponibles même si certaines échouent

**Avantages** :
- ✅ **Robustesse** : Compense les faiblesses de chaque méthode individuelle
- ✅ **Personnalisation maximale** : Combine filtrage collaboratif + contenu + tendances
- ✅ **Consensus intelligent** : Bonus pour articles recommandés par plusieurs méthodes
- ✅ **Diversité garantie** : Encourage l'exploration de nouvelles catégories

**Configuration** : Ajustez `HYBRID_WEIGHTS` dans [config.py](backend/config.py) pour changer les pondérations

---

## 🆕 Gestion du cold start

Le système implémente une stratégie complète pour gérer le **cold start**, c'est-à-dire l'arrivée de nouveaux utilisateurs et de nouveaux articles sans historique suffisant.

### 🧑 Cold start utilisateurs

#### Détection intelligente

Le système utilise une **approche en deux étapes** pour détecter si un utilisateur a suffisamment d'historique :

1. **Vérification quantitative** : Minimum **5 articles uniques** lus (configurable via `MIN_UNIQUE_ARTICLES_READ`)
2. **Validation qualitative** : Les articles doivent exister dans les métadonnées (IDs valides)

**Exemple** : Un utilisateur avec 50 clics sur le même article = 1 seul article unique → historique insuffisant

#### Scénarios de recommandation

| Phase utilisateur | Articles uniques lus | Comportement système |
|------------------|---------------------|---------------------|
| **Nouvel utilisateur** | 0 | Fallback automatique vers **popularité avec boost nouveauté** |
| **Peu d'historique** | 1-4 | Fallback automatique vers **popularité avec boost nouveauté** |
| **Historique suffisant** | ≥5 | Recommandations **personnalisées complètes** (4 méthodes disponibles) |

#### Comportement par méthode

| Méthode | Utilisateur avec historique | Utilisateur sans historique |
|---------|----------------------------|----------------------------|
| **🔥 Popularité** | Tendances actuelles | Tendances actuelles (fonctionne directement) |
| **📖 Contenu** | Similarité basée embeddings | Fallback → Popularité avec boost |
| **👥 Clustering** | Articles populaires du segment | Fallback → Popularité avec boost |
| **🎭 Hybride** | Combinaison des 3 méthodes | Fallback → Popularité avec boost |

**Avantages** :
- ✅ **Aucune erreur** : Toujours des recommandations pertinentes
- ✅ **Transition progressive** : Personnalisation croissante avec l'accumulation d'historique
- ✅ **Robustesse** : Gestion automatique des données invalides

---

### 📄 Cold start articles

#### Stratégies implémentées

Le système utilise **3 stratégies complémentaires** pour garantir la visibilité des nouveaux articles :

**1️⃣ Boost temporaire de nouveauté** (Méthode Popularité)

Les nouveaux articles reçoivent un multiplicateur de score automatique :
- **< 24h** : ×1.5 (+50% de visibilité)
- **24-72h** : ×1.2 (+20% de visibilité)
- **> 72h** : ×1.0 (score normal)

**Exemple** :
```
Article ancien (8 mois, 800 clics) : score = 100 clics/mois
Article récent (1 jour, 10 clics) : score = 333 × 1.5 = 500 clics/mois équivalents
→ Le nouvel article surpasse l'ancien grâce au boost
```

**2️⃣ Endpoint dédié "Articles récents"** (`GET /articles/recent`)

Un endpoint spécifique permet de récupérer les nouveaux articles indépendamment des clics :
- Fenêtre temporelle configurable (défaut : 48h)
- Filtrage par catégorie optionnel
- Idéal pour une section "Nouveautés" dans l'interface

**3️⃣ Fallback métadonnées** (Méthode Similarité de contenu)

Si les embeddings ne sont pas disponibles pour un article, le système utilise :
- Les **3 catégories préférées** de l'utilisateur
- La **longueur d'articles** préférée (`words_count`)
- Scoring par similarité de métadonnées avec bonus pour catégories favorites

#### Impact sur les méthodes de recommandation

| Méthode | Article avec embeddings | Article sans embeddings | Article sans clics |
|---------|------------------------|------------------------|--------------------|
| **🔥 Popularité** | Score normal + boost nouveauté | Score normal + boost nouveauté | Boost ×1.5 compense le 0 clic |
| **📖 Contenu** | Similarité embeddings | Fallback métadonnées | Fallback métadonnées |
| **👥 Clustering** | Popularité dans segment | Popularité dans segment | Popularité dans segment |
| **🎭 Hybride** | Combinaison complète | Fallback métadonnées + popularité | Bénéficie du boost via popularité |

**Avantages** :
- ✅ **Visibilité immédiate** : Les nouveaux articles apparaissent dès publication
- ✅ **Dégradé progressif** : Le boost diminue naturellement avec le temps
- ✅ **Robustesse** : Fonctionne même sans embeddings calculés

### 📊 Tableau récapitulatif

| Aspect | Nouvel utilisateur | Nouvel article |
|--------|-------------------|----------------|
| **Détection** | < 5 articles uniques lus | Âge < 72h ou embeddings manquants |
| **Stratégie** | Fallback popularité | Boost ×1.5 + endpoint dédié + fallback métadonnées |
| **Délai visibilité** | Immédiat | Immédiat |
| **Transition** | Progressive (5+ articles) | Progressive (3 jours) |
| **Configuration** | `MIN_UNIQUE_ARTICLES_READ` | `NOVELTY_BOOST_24H`, `NOVELTY_BOOST_72H` |

---

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

---

### API REST complète

- **Documentation interactive** automatique avec FastAPI (Swagger UI disonible à `/docs`)
- **Gestion d'erreurs** robuste avec codes HTTP appropriés
- **Validation automatique** des paramètres avec Pydantic
- **Support CORS** pour l'intégration frontend
- **Endpoints de debug** pour le monitoring et les tests

## 🚀 Lancement du backend de l'application

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

## 🔌 API - Endpoints et utilisation

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
  "actual_method": "hybrid",
  "fallback_applied": false,
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
    "requested_method": "hybrid",
    "actual_method": "hybrid",
    "fallback_applied": false,
    "fallback_reason": null,
    "user_stats": {
      "user_id": 12345,
      "total_interactions": 23,
      "unique_articles": 20,
      "is_new_user": false
    }
  },
  "generated_at": "2025-09-30T14:30:00"
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

#### 📰 Articles récents (Cold start nouveaux articles)
```http
GET /articles/recent?hours=48&category_id=281&limit=10
```
Retourne les articles les plus récents publiés dans une fenêtre temporelle donnée.

**Paramètres :**
- `hours` : Fenêtre temporelle en heures (défaut: 48h)
- `category_id` : Filtrer par catégorie (optionnel)
- `limit` : Nombre maximum d'articles (max 50)

**Exemple de réponse :**
```json
[
  {
    "rank": 1,
    "article_id": 364046,
    "created_date": "2018-03-13T15:30:00",
    "category_id": 281,
    "words_count": 195,
    "age_hours": 2,
    "metadata": {
      "article_id": 364046,
      "category_id": 281,
      "words_count": 195,
      "created_date": "2018-03-13T15:30:00"
    }
  }
]
```

### Endpoints de debug

#### ⚙️ Configuration actuelle
```http
GET /debug/config
```

#### 📈 Statistiques détaillées des données
```http
GET /debug/data-stats
```

## 🧪 Tests et validation

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

# Articles récents (Cold start nouveaux articles)
curl "http://localhost:8000/articles/recent"
curl "http://localhost:8000/articles/recent?hours=24&limit=20"
curl "http://localhost:8000/articles/recent?category_id=281&hours=48"

# Statistiques détaillées des données (debug)
curl http://localhost:8000/debug/data-stats
```

### Interface de documentation interactive

Accédez à http://localhost:8000/docs pour :
- Voir tous les endpoints disponibles
- Tester directement l'API depuis le navigateur
- Consulter les schémas de données
- Voir les exemples de requêtes/réponses

## 🏗️ Architecture technique

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

## ⚙️ Configuration et personnalisation

### Paramètres principaux (config.py)

```python
MAX_ARTICLE_AGE_DAYS = 730       # Âge maximum des articles (jours)
MIN_WORDS_COUNT = 50             # Nombre minimum de mots par article
N_USER_CLUSTERS = 5              # Nombre de segments utilisateurs
MIN_UNIQUE_ARTICLES_READ = 5     # Seuil pour cold start (articles uniques lus requis)
                                 # Valeurs recommandées : 3 (permissif), 5 (équilibré), 10 (conservateur)

# Poids de l'approche hybride
HYBRID_WEIGHTS = {
    "clustering": 0.4,           # Filtrage collaboratif
    "content": 0.3,              # Similarité de contenu
    "popularity": 0.2,           # Popularité normalisée par âge
    "diversity": 0.1             # Bonus diversité
}

# Cold start pour nouveaux articles
NOVELTY_BOOST_24H = 1.5          # Boost pour articles < 24h (+50%)
NOVELTY_BOOST_72H = 1.2          # Boost pour articles 24-72h (+20%)
RECENT_ARTICLES_CUTOFF_HOURS = 48  # Fenêtre pour endpoint /articles/recent
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

## 📈 Monitoring et logs

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

## 🚀 Recommandations pour la mise en production

Cette section présente les bonnes pratiques et adaptations nécessaires pour déployer ce système de recommandation en environnement de production réel.

### Infrastructure et base de données

#### Choix de la base de données

| Composant | Technologie recommandée | Justification |
|-----------|------------------------|---------------|
| **Base principale** | **PostgreSQL 15+** | Support natif des vecteurs (pgvector), transactions ACID, maturité |
| **Cache** | **Redis** | Performance pour données chaudes (embeddings fréquents, scores) |
| **Queue** | **Celery + Redis** | Traitement asynchrone (génération embeddings, recalcul clusters) |
| **Monitoring** | **Prometheus + Grafana** | Métriques temps réel (latence, taux de cold start, etc.) |

#### Schéma de données recommandé

**Tables essentielles** :
- `articles` : Métadonnées + embeddings (type `VECTOR(250)` avec pgvector)
- `clicks` : Interactions utilisateur-article (indexées sur `user_id`, `article_id`, `timestamp`)
- `user_clusters` : Assignations cluster-utilisateur (mise à jour quotidienne)
- Vue matérialisée `article_popularity` : Précalcul des scores de popularité (rafraîchie toutes les heures)

### Pipeline de génération d'embeddings

#### Stratégie recommandée

**Pour les nouveaux articles** :

1. **Publication article** : Insertion dans table `articles` avec `embedding = NULL`
2. **Queue asynchrone** : Tâche Celery envoyée au service d'embeddings
3. **Génération** : API dédiée avec GPU (Sentence-BERT multilingual)
4. **Mise à jour** : `UPDATE articles SET embedding = ... WHERE article_id = ...`

**Temps de traitement estimés** :
- Génération : ~50-100ms par article (avec GPU)
- Traitement batch : ~1000 articles/minute

**Fallback pendant génération** :
- Utiliser le système de **recommandation par métadonnées (catégories + longueur)**
- Le **boost de nouveauté** garantit la visibilité immédiate via **popularité**

#### Technologies recommandées

- **Modèle** : Sentence-BERT (`sentence-transformers/paraphrase-multilingual-mpnet-base-v2`)
- **Infrastructure** : AWS Lambda avec GPU ou Azure Functions Premium
- **Coût** : ~$0.10 pour 1000 articles (estimation AWS)

### Autres recommandations

- **Stockage des embeddings** : PostgreSQL + pgvector
- **Pipeline d'embeddings asynchrone** : Celery + Redis
- **Clusters utilisateurs** : recalcul quotidien via tâche planifiée (cron job ou Celery beat)
- **Monitoring** : Prometheus + Grafana
- **Sécurité** : authentification API (OAuth2/JWT), HTTPS obligatoire
- **Documentation** : API à jour (Swagger)
- **Taux de cold start** : < 20%
- **Génération embeddings** : < 2min de delay
- **Stabilité clusters** : réassignation < 10%
- **Distribution des méthodes** : à analyser
- **Feedback utilisateur** : à collecter (like/dislike)

---

## 📝 Conclusion

Ce système de recommandation implémente une architecture complète et robuste, prête pour la production. Les stratégies de cold start garantissent une expérience utilisateur optimale dès le premier jour, tandis que les recommandations personnalisées s'améliorent progressivement avec l'accumulation de données.

**Points forts du système** :
- ✅ 4 méthodes complémentaires (popularité, contenu, clustering, hybride)
- ✅ Gestion automatique du cold start (utilisateurs ET articles)
- ✅ Fallbacks intelligents (métadonnées, boost nouveauté)
- ✅ Architecture évolutive et maintenable
- ✅ Documentation complète et API REST moderne

**Prochaines étapes** :
1. Déploiement en environnement de staging
2. Tests A/B sur échantillon d'utilisateurs (10%)
3. Optimisation des pondérations hybrides
4. Intégration du feedback utilisateur explicite (like/dislike)
5. Exploration de modèles plus avancés (transformers, GNNs)

