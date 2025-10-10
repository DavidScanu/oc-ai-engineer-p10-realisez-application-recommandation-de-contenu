# Déploiement Backend sur Azure App Service

Guide simplifié basé sur le déploiement réel en production avec **P1V2 Premium**.

## ✅ Déploiement en Production

**URL** : `https://my-content-api-oc.azurewebsites.net`

**Configuration** :
- Plan : **P1V2 Premium** (3.5GB RAM, ~150€/mois)
- Runtime : Python 3.11, France Central
- Workers : 2, Timeout : 120s

**Performances** :
- `/health` : ~15s (1ère fois), < 1s ensuite
- Recommendations : ~8s (1ère fois), < 1s ensuite

---

## Déploiement complet

### 1. Préparation
```bash
cd backend
az login
az provider register --namespace Microsoft.Web
az provider show --namespace Microsoft.Web --query "registrationState"
```

### 2. Créer le resource group (optionnel - créé automatiquement par az webapp up)

```bash
# Vérifier si le resource group existe
az group exists --name my-content-rg

# Si besoin, créer manuellement le resource group
az group create \
  --name my-content-rg \
  --location francecentral

# Lister les resource groups
az group list --output table
```

**Note** : La commande `az webapp up` (étape suivante) crée automatiquement le resource group s'il n'existe pas. Cette étape est donc optionnelle.

### 3. Créer l'infrastructure P1V2
```bash
az webapp up \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --runtime "PYTHON:3.11" \
  --location francecentral \
  --sku P1V2 \
  --logs
```
**Note** : Timeout normal après ~10min. L'infrastructure est créée, passez à l'étape suivante.

### 4. Déployer via ZIP
```bash
zip -r backend-deploy.zip . -x "*.git*" "__pycache__/*" "*.pyc" ".venv/*" "*.log" "data-analysis/*" "scripts/*"

az webapp deployment source config-zip \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --src backend-deploy.zip

rm backend-deploy.zip
```
Durée : 5-10min upload + 8min build

### 5. Configuration
```bash
az webapp config set \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --startup-file "startup.sh"

az webapp config appsettings set \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --settings \
    "ALLOWED_ORIGINS=http://localhost:3000" \
    "GUNICORN_WORKERS=2" \
    "GUNICORN_TIMEOUT=120" \
    "GUNICORN_LOG_LEVEL=info"
```

### 6. Test
```bash
az webapp restart --name my-content-api-oc --resource-group my-content-rg
sleep 60
curl https://my-content-api-oc.azurewebsites.net/health
```

---

## Logs

**Temps réel** :
```bash
az webapp log tail --name my-content-api-oc --resource-group my-content-rg
```

**Télécharger** :
```bash
az webapp log download --name my-content-api-oc --resource-group my-content-rg --log-file logs.zip
```

---

## Mise à jour

```bash
cd backend
zip -r backend-deploy.zip . -x "*.git*" "__pycache__/*" "*.pyc" ".venv/*" "*.log" "data-analysis/*" "scripts/*"
az webapp deployment source config-zip --name my-content-api-oc --resource-group my-content-rg --src backend-deploy.zip
rm backend-deploy.zip
az webapp restart --name my-content-api-oc --resource-group my-content-rg
```

---

## Pourquoi P1V2 ?

| Plan | RAM | Résultat |
|------|-----|----------|
| B1 Basic | 1.75GB | ❌ Workers killed (OOM) |
| S1 Standard | 1.75GB | ⚠️ Timeouts |
| **P1V2 Premium** | **3.5GB** | ✅ **Stable** |

Les embeddings (348MB) + code + 2 workers nécessitent **3GB+ RAM**.

---

## Supprimer l'application

### Option 1 : Supprimer uniquement l'App Service (conserver le resource group)

```bash
# Supprimer l'application
az webapp delete \
  --name my-content-api-oc \
  --resource-group my-content-rg

# Vérifier la suppression
az webapp list --resource-group my-content-rg --output table
```

### Option 2 : Supprimer tout le resource group (recommandé)

⚠️ **Attention** : Cela supprime **tout** (App Service + App Service Plan + logs + tous les services du groupe).

```bash
# Lister ce qui sera supprimé
az resource list --resource-group my-content-rg --output table

# Supprimer tout le resource group
az group delete \
  --name my-content-rg \
  --yes \
  --no-wait

# Vérifier la suppression (peut prendre quelques minutes)
az group exists --name my-content-rg
```

**Résultat** : `false` signifie que le groupe est supprimé.

### Option 3 : Supprimer uniquement l'App Service Plan (pour réduire les coûts)

```bash
# Récupérer le nom du plan
az appservice plan list --resource-group my-content-rg --output table

# Supprimer le plan (supprime aussi l'App Service associé)
az appservice plan delete \
  --name davidscanu14_asp_0798 \
  --resource-group my-content-rg \
  --yes
```

### Vérification de la facturation

```bash
# Voir les coûts actuels
az consumption usage list --query "[?contains(instanceName, 'my-content-api')].{Name:instanceName, Cost:pretaxCost, Date:usageStart}" --output table
```

**Conseil** : Pour arrêter la facturation complètement, utilisez l'**Option 2** (supprimer le resource group).

---

## Résumé des commandes

### Déploiement complet
```bash
cd backend
az login
az provider register --namespace Microsoft.Web

# (Optionnel) Créer le resource group manuellement
az group create --name my-content-rg --location francecentral

# Créer l'infrastructure et déployer
az webapp up --name my-content-api-oc --resource-group my-content-rg --runtime "PYTHON:3.11" --location francecentral --sku P1V2 --logs
zip -r backend-deploy.zip . -x "*.git*" "__pycache__/*" "*.pyc" ".venv/*" "*.log" "data-analysis/*" "scripts/*"
az webapp deployment source config-zip --name my-content-api-oc --resource-group my-content-rg --src backend-deploy.zip
rm backend-deploy.zip
az webapp config set --name my-content-api-oc --resource-group my-content-rg --startup-file "startup.sh"
az webapp config appsettings set --name my-content-api-oc --resource-group my-content-rg --settings "ALLOWED_ORIGINS=http://localhost:3000" "GUNICORN_WORKERS=2" "GUNICORN_TIMEOUT=120"
az webapp restart --name my-content-api-oc --resource-group my-content-rg
```

### Suppression complète
```bash
# Supprimer tout le resource group
az group delete --name my-content-rg --yes --no-wait
az group exists --name my-content-rg  # Vérifier : doit retourner 'false'

# Voir l'état de la suppression
az group show --name my-content-rg --query "properties.provisioningState"

# Vérifier que le resource group est bien supprimé
az group exists --name my-content-rg
# Doit retourner : false

# Lister tous vos resource groups pour confirmer
az group list --output table

# Voir les coûts (peut prendre 24-48h pour se mettre à jour)
az consumption usage list --output table
```
