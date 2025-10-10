# 🚀 Guide de démarrage rapide - My Content

## Démarrage complet (Backend + Frontend)

### Prérequis
- Python 3.11+
- Node.js 20+
- Git LFS configuré

### Option 1 : Scripts automatiques (Recommandé)

```bash
# 1. Cloner et préparer le projet
git clone <repo-url>
cd oc-ai-engineer-p10-realisez-application-recommandation-de-contenu
git lfs pull

# 2. Terminal 1 - Démarrer le backend
cd backend
chmod +x start.sh
./start.sh
# ✓ Backend disponible sur http://localhost:8000

# 3. Terminal 2 - Démarrer le frontend
cd frontend
chmod +x start.sh
./start.sh
# ✓ Frontend disponible sur http://localhost:3000
```

### Option 2 : Manuelle

**Backend** :
```bash
cd backend

# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'API
uvicorn main:app --reload
```

**Frontend** :
```bash
cd frontend

# Installer les dépendances
npm install

# Configurer l'environnement
cp .env.example .env.local

# Démarrer le serveur
npm run dev
```

## ✅ Vérification

1. **Backend** : Ouvrir [http://localhost:8000/docs](http://localhost:8000/docs)
   - Vous devez voir l'interface Swagger interactive

2. **Frontend** : Ouvrir [http://localhost:3000](http://localhost:3000)
   - L'application doit charger avec la liste des utilisateurs

3. **Test rapide** :
   ```bash
   # Backend health check
   curl http://localhost:8000/health

   # Recommandations test
   curl -X POST "http://localhost:8000/recommend/5890?method=hybrid&n_recommendations=5"
   ```

## 🎯 Utilisation de l'application

### Page principale (/)

1. **Sélectionner un utilisateur** dans le dropdown
2. **Choisir une méthode** :
   - 🎭 Hybride (par défaut) - Meilleure qualité
   - 🔥 Popularité - Articles tendances
   - 📖 Contenu - Similarité textuelle
   - 👥 Clustering - Filtrage collaboratif
3. **Voir les recommandations** - 5 articles affichés avec détails
4. **Vérifier le fallback** - Alerte jaune si méthode de repli appliquée

### Page Insights (/insights)

1. Cliquer sur **"Insights"** dans le header
2. Onglet **"Populaires"** : Top 10 des articles avec le meilleur score
3. Onglet **"Récents"** : Nouveaux articles des 48h

## 🔧 Commandes utiles

### Backend
```bash
# Démarrage rapide
./start.sh

# Tester l'API
python3 scripts/test_api.py

# Cold start test
python3 scripts/test_cold_start.py

# Analyse de données
python3 data-analysis/analyze_data.py
```

### Frontend
```bash
# Développement
npm run dev

# Build production
npm run build
npm start

# Linting
npm run lint
```

## 🐛 Problèmes courants

### "Backend not responding"
```bash
# Vérifier que le backend tourne
curl http://localhost:8000/health

# Si erreur, redémarrer
cd backend
./start.sh
```

### "Cannot connect to API"
```bash
# Vérifier .env.local
cat frontend/.env.local
# Doit contenir: NEXT_PUBLIC_API_URL=http://localhost:8000

# Recréer si nécessaire
cp .env.example .env.local
```

### "Port already in use"
```bash
# Backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

### "No recommendations"
```bash
# Vérifier l'utilisateur
curl http://localhost:8000/users/5890/stats

# Tester avec un utilisateur connu
# Utilisateurs avec bon historique: 5890, 7654, 12345
```

## 📊 Données de test

### Utilisateurs recommandés pour tests

| User ID | Historique | Type | Idéal pour tester |
|---------|-----------|------|------------------|
| 5890 | 23 articles | Normal | Toutes les méthodes |
| 7654 | 15 articles | Actif | Hybride, Clustering |
| 1 | 2 articles | Nouveau | Fallback (cold start) |
| 322897 | 1 article | Nouveau | Fallback (cold start) |

### Méthodes par scénario

**Utilisateur actif (>10 articles)** :
- ✅ Hybride - Meilleure qualité
- ✅ Contenu - Personnalisé
- ✅ Clustering - Découverte
- ✅ Popularité - Tendances

**Nouvel utilisateur (<5 articles)** :
- ⚠️ Hybride → Fallback Popularité
- ⚠️ Contenu → Fallback Popularité
- ⚠️ Clustering → Fallback Popularité
- ✅ Popularité - Fonctionne directement

## 🚀 Déploiement

### Backend (Azure Functions)
```bash
# Voir backend/README.md section déploiement
# Configuration Azure Functions
```

### Frontend (Vercel)
```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
cd frontend
vercel

# Configurer les variables d'environnement
# NEXT_PUBLIC_API_URL=https://votre-backend-url.azurewebsites.net
```

## 🎓 Architecture

```
┌─────────────┐         ┌──────────────┐
│   Browser   │ ◄─────► │   Next.js    │
│ localhost:  │  HTTP   │  Frontend    │
│    3000     │         │ (TypeScript) │
└─────────────┘         └──────┬───────┘
                                │
                                │ REST API
                                ▼
                        ┌──────────────┐
                        │   FastAPI    │
                        │   Backend    │
                        │   (Python)   │
                        │ localhost:   │
                        │    8000      │
                        └──────┬───────┘
                                │
                                ▼
                        ┌──────────────┐
                        │    Data      │
                        │  - Articles  │
                        │  - Clicks    │
                        │ - Embeddings │
                        └──────────────┘
```

## ✅ Checklist de démarrage

- [ ] Git LFS installé et configuré
- [ ] Python 3.11+ installé
- [ ] Node.js 20+ installé
- [ ] Dépôt cloné
- [ ] `git lfs pull` exécuté
- [ ] Backend démarré (http://localhost:8000/docs accessible)
- [ ] Frontend démarré (http://localhost:3000 accessible)
- [ ] Test d'une recommandation réussi
- [ ] Page Insights fonctionne
