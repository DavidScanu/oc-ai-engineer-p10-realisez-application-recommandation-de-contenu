# Scripts de test de l'API de recommandation

Ce dossier contient des scripts de test pour valider le bon fonctionnement de l'API de recommandation.

## 📋 Scripts disponibles

### 1. `test_api.py` - Tests généraux
Script de test complet pour valider le fonctionnement général de l'API.

**Utilisation :**
```bash
cd backend
python scripts/test_api.py
```

**Ce qui est testé :**
- ✅ Health check de l'API
- ✅ Récupération de la liste des utilisateurs
- ✅ Statistiques d'un utilisateur
- ✅ Toutes les méthodes de recommandation (popularity, content, clustering, hybrid)
- ✅ Articles populaires

---

### 2. `test_cold_start.py` - Tests du cold start (NOUVEAU) 🆕
Script spécialisé pour valider la détection intelligente du cold start avec validation des interactions.

**Utilisation :**
```bash
cd backend
python scripts/test_cold_start.py
```

**Ce qui est testé :**

#### Test 1 : Utilisateur inexistant (0 interactions)
- ✅ Vérifie que les méthodes `content`, `clustering`, `hybrid` font un **fallback vers popularity**
- ✅ Vérifie que la méthode `popularity` fonctionne **sans fallback**
- ✅ Valide la présence des métadonnées de fallback (`fallback_applied`, `fallback_from`, `fallback_reason`)

#### Test 2 : Utilisateur avec peu d'interactions (< 5)
- ✅ Cherche automatiquement un utilisateur avec 1-4 interactions dans la base
- ✅ Vérifie que **tous les fallbacks sont appliqués** même si l'utilisateur a un historique
- ✅ Valide le seuil `MIN_USER_INTERACTIONS = 5`

#### Test 3 : Utilisateur avec interactions suffisantes (≥ 5)
- ✅ Cherche automatiquement un utilisateur avec ≥5 interactions
- ✅ Vérifie que les méthodes personnalisées fonctionnent **sans fallback**
- ✅ Valide que les recommandations sont bien personnalisées

**Validations effectuées pour chaque test :**
- 🔍 Cohérence `fallback_applied` vs comportement attendu
- 🔍 Cohérence `actual_method` vs méthode demandée
- 🔍 Présence de recommandations (liste non vide)
- 🔍 Présence des champs de métadonnées (`fallback_reason`, `fallback_from`)
- 🔍 Format des réponses conforme à l'API

**Sortie attendue :**
```
================================================================================
  🧪 TESTS DE VALIDATION DU COLD START
  Validation de la détection intelligente et des fallbacks
================================================================================

ℹ️  Vérification de la disponibilité de l'API...
✅ API disponible

================================================================================
TEST 1: Utilisateur inexistant (Cold Start Total)
================================================================================

ℹ️  Test avec user_id=999999999 (inexistant)

  📈 Statistiques utilisateur:
     • Total interactions: 0
     • Articles uniques: 0
     • Nouvel utilisateur: True

  📊 Résultats pour méthode 'content':
     • Fallback appliqué: True
     • Méthode réelle: popularity
     • Nombre de recommandations: 5
     • Raison du fallback: Cold start: utilisateur sans historique...
     • Fallback détecté depuis: content
     • Raison courte: insufficient_valid_history

✅ Test réussi pour méthode 'content'
[... autres méthodes ...]

✅ ✨ TEST 1 RÉUSSI: Tous les fallbacks fonctionnent correctement

[... autres tests ...]

================================================================================
RÉSUMÉ FINAL DES TESTS
================================================================================

  Test                                              Résultat
  -------------------------------------------------- ---------------
  Test 1: Utilisateur inexistant                    ✅ RÉUSSI
  Test 2: Peu d'interactions                        ✅ RÉUSSI
  Test 3: Interactions suffisantes                  ✅ RÉUSSI

  -------------------------------------------------- ---------------

  📊 Taux de réussite: 3/3 (100.0%)

✅ 🎉 TOUS LES TESTS SONT PASSÉS !
```

---

## 🚀 Prérequis

### Installation des dépendances
```bash
pip install -r requirements.txt
```

Les dépendances de test incluent :
- `requests` : Pour les appels HTTP à l'API
- `colorama` : Pour l'affichage coloré dans le terminal

### API en cours d'exécution
Assurez-vous que l'API est démarrée avant de lancer les tests :
```bash
# Dans un terminal séparé
cd backend
python main.py
# ou
uvicorn main:app --reload
```

L'API doit être accessible sur `http://localhost:8000`

---

## 📊 Interprétation des résultats

### Codes de couleur
- 🟢 **Vert (✅)** : Test réussi
- 🔴 **Rouge (❌)** : Test échoué
- 🟡 **Jaune (ℹ️)** : Information
- 🟣 **Magenta (⚠️)** : Avertissement ou test ignoré

### Cas d'échec possibles

#### Test 1 échoue
**Problème** : Le fallback ne se déclenche pas pour un utilisateur inexistant
**Causes possibles** :
- La condition `_has_sufficient_history()` n'est pas utilisée
- `MIN_USER_INTERACTIONS` est configuré à 0

#### Test 2 échoue
**Problème** : Les utilisateurs avec < 5 interactions ne déclenchent pas le fallback
**Causes possibles** :
- `MIN_USER_INTERACTIONS` est < 1
- La validation des `click_article_id` n'est pas appliquée

#### Test 3 échoue
**Problème** : Les utilisateurs avec ≥ 5 interactions déclenchent un fallback
**Causes possibles** :
- Les `click_article_id` sont invalides (pas dans les métadonnées)
- Le seuil `MIN_USER_INTERACTIONS` est trop élevé

---

## 🔧 Configuration

### Modifier l'URL de l'API
Si votre API tourne sur un port différent :
```bash
# Dans le script
tester = ColdStartTester(base_url="http://localhost:8080")
```

### Modifier les seuils testés
Pour tester avec un seuil différent de 5, modifiez `MIN_USER_INTERACTIONS` dans `backend/config.py` :
```python
MIN_USER_INTERACTIONS: int = 10  # Exemple: seuil plus conservateur
```

Puis relancez les tests.

---

## 🐛 Débogage

### L'API ne répond pas
```bash
curl http://localhost:8000/health
```

Si pas de réponse, vérifiez que l'API est bien démarrée.

### Erreurs HTTP 500
Consultez les logs de l'API (terminal où `main.py` tourne) pour voir les erreurs détaillées.

### Aucun utilisateur trouvé pour Test 2/3
C'est possible si votre dataset n'a pas d'utilisateurs dans la plage testée. Le script l'indiquera avec un avertissement.

---

## 📝 Ajout de nouveaux tests

Pour ajouter un nouveau scénario de test, créez une méthode dans `ColdStartTester` :

```python
def test_scenario_4_custom(self):
    """Test 4: Description de votre test"""
    self.print_section("TEST 4: Titre de votre test")

    # Votre logique de test
    user_id = 12345
    passed = self.test_recommendation(user_id, "hybrid", expected_fallback=True)

    # Enregistrer le résultat
    self.test_results.append(("Test 4: Custom", passed))
    return passed
```

Puis appelez-le dans `run_all_tests()` :
```python
def run_all_tests(self):
    # ... tests existants ...
    self.test_scenario_4_custom()
    # ...
```

---

## 📚 Références

- Documentation de l'API : http://localhost:8000/docs
- Configuration : `backend/config.py`
- Implémentation du cold start : `backend/recommenders/base.py`