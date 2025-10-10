# Déploiement Backend sur Azure App Service

Guide complet pour déployer l'API FastAPI My Content sur Azure App Service.

## ✅ Déploiement en Production

**URL de production** : `https://my-content-api-oc.azurewebsites.net`

**Configuration actuelle** :
- Plan : **P1V2 Premium** (1 core, 3.5GB RAM, ~150€/mois)
- Runtime : Python 3.11
- Région : France Central
- Workers Gunicorn : 2
- Startup command : `startup.sh`
- CORS : `http://localhost:3000`

**État** : ✅ Déployé et fonctionnel

**Performances mesurées** :
- Root endpoint `/` : < 1s
- Health check `/health` : ~15s (première fois), < 1s ensuite
- Recommendations popularity : < 1s
- Recommendations content-based : ~8s (première fois avec chargement embeddings), < 1s ensuite
- Recommendations hybrid : ~8s (première fois), < 1s ensuite

## Prérequis

1. **Compte Azure** avec une souscription active
2. **Azure CLI** installé localement

### Installation d'Azure CLI (Linux/WSL)

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Vérification :
```bash
az --version
az login
```

## Option 1 : Déploiement via Azure CLI (Recommandé)

### Étape 1 : Préparation

```bash
cd backend

# Se connecter à Azure
az login

# Lister vos souscriptions
az account list --output table

# Sélectionner la bonne souscription (si vous en avez plusieurs)
az account set --subscription "VOTRE_SUBSCRIPTION_ID"

# Enregistrer le provider Microsoft.Web (première fois uniquement)
az provider register --namespace Microsoft.Web

# Vérifier l'enregistrement (attendre "Registered")
az provider show --namespace Microsoft.Web --query "registrationState"
```

### Étape 2 : Déploiement initial (peut timeout - c'est normal)

```bash
# Déployer avec az webapp up (crée automatiquement les ressources)
# Note : Si westeurope n'est pas disponible, essayez francecentral, northeurope ou uksouth
# ⚠️ Commencez par B1 pour tester, puis upgradez vers S1 (voir étape suivante)
az webapp up \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --runtime "PYTHON:3.11" \
  --location francecentral \
  --sku B1 \
  --logs
```

**Note** : Cette commande peut timeout lors de l'upload des 360MB de données (embeddings). C'est normal, l'application continue de se déployer en arrière-plan.

**Régions alternatives** si la région choisie n'accepte pas de nouveaux clients :
- `francecentral` (France Central - Paris)
- `northeurope` (North Europe - Irlande)
- `uksouth` (UK South - Londres)
- `westus2` (West US 2 - États-Unis)

Pour voir toutes les régions disponibles :
```bash
az account list-locations --query "[?metadata.regionCategory=='Recommended'].{Name:name, DisplayName:displayName}" --output table
```

**Paramètres :**
- `--name` : Nom de votre App Service (doit être unique globalement)
- `--resource-group` : Groupe de ressources (créé automatiquement)
- `--runtime` : Python 3.11
- `--location` : Région Azure (westeurope, francecentral, etc.)
- `--sku` : Plan tarifaire (B1 = Basic, ~13€/mois)
- `--logs` : Active les logs de streaming

### Étape 2bis : Redéploiement via zip (si timeout à l'étape 2)

Si `az webapp up` a timeout, redéployez manuellement via zip :

```bash
cd backend

# Créer le zip du code
zip -r backend-deploy.zip . -x "*.git*" "__pycache__/*" "*.pyc" ".venv/*" "*.log" "data-analysis/*" "scripts/*"

# Déployer le zip (prend 5-10 minutes pour 360MB)
az webapp deployment source config-zip \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --src backend-deploy.zip

# Nettoyer
rm backend-deploy.zip
```

**Important** : Le build prendra environ 8 minutes. Attendez le message `Build successful` avant de continuer.

### Étape 3 : Configuration du startup command

```bash
az webapp config set \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --startup-file "startup.sh"
```

### Étape 4 : Configuration des variables d'environnement

```bash
az webapp config appsettings set \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --settings \
    "ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app" \
    "GUNICORN_WORKERS=1" \
    "GUNICORN_TIMEOUT=120" \
    "GUNICORN_LOG_LEVEL=info"
```

**Note** : On démarre avec 1 worker car le plan B1 a peu de RAM. On upgradra vers S1 avec 2 workers ensuite.

### Étape 5 : Tester le déploiement B1

```bash
# Redémarrer l'application
az webapp restart --name my-content-api-oc --resource-group my-content-rg

# Attendre 60 secondes puis tester
sleep 60
curl https://my-content-api-oc.azurewebsites.net/

# Tester le health check (peut prendre 30s au premier appel)
curl https://my-content-api-oc.azurewebsites.net/health
```

### Étape 6 : ⚠️ IMPORTANT - Upgrade vers S1 Standard (Recommandé)

Le plan **B1 Basic (1.75GB RAM)** est **insuffisant** pour ce projet. Les workers Gunicorn sont tués par manque de mémoire lors du chargement des embeddings (348MB).

**Solution : Upgrader vers S1 Standard** (~60€/mois au lieu de ~13€/mois) :

```bash
# Récupérer le nom du plan (généralement davidscanu14_asp_XXXX)
az appservice plan list --resource-group my-content-rg --query "[0].name" -o tsv

# Upgrader vers S1 Standard
az appservice plan update \
  --name <NOM_DU_PLAN> \
  --resource-group my-content-rg \
  --sku S1

# Augmenter les workers à 2
az webapp config appsettings set \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --settings "GUNICORN_WORKERS=2"

# Redémarrer
az webapp restart --name my-content-api-oc --resource-group my-content-rg
```

### Étape 7 : Vérification finale

```bash
# Attendre 60 secondes que l'app redémarre avec le nouveau plan
sleep 60

# Tester le root endpoint
curl https://my-content-api-oc.azurewebsites.net/

# Tester le health check (peut prendre 20-30s au premier appel)
curl https://my-content-api-oc.azurewebsites.net/health

# Tester une recommandation
curl -X POST "https://my-content-api-oc.azurewebsites.net/recommend/5890?method=popularity&n_recommendations=3"
```

**Note importante** : Le premier appel à `/health` ou aux méthodes utilisant les embeddings (content-based, hybrid) prend 20-60 secondes pour charger les 348MB de données en mémoire. Après le premier appel, les données restent en cache et les réponses sont quasi instantanées.

### Étape 8 : Activer les logs (optionnel)

```bash
# Activer les logs d'application
az webapp log config \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --application-logging filesystem \
  --level information

# Streamer les logs en temps réel
az webapp log tail \
  --name my-content-api-oc \
  --resource-group my-content-rg
```

## Option 2 : Déploiement via le Portail Azure

### Étape 1 : Créer l'App Service

1. Aller sur https://portal.azure.com
2. Cliquer sur "Créer une ressource" → "Web App"
3. Configuration :
   - **Subscription** : Votre souscription
   - **Resource Group** : Créer nouveau "my-content-rg"
   - **Name** : my-content-api (doit être unique)
   - **Publish** : Code
   - **Runtime stack** : Python 3.11
   - **Operating System** : Linux
   - **Region** : West Europe (ou France Central)
   - **Pricing plan** : Basic B1
4. Cliquer sur "Review + Create" puis "Create"

### Étape 2 : Configurer le déploiement

1. Aller dans votre App Service → **Deployment Center**
2. Choisir votre source :
   - **GitHub** : Sélectionner votre repo et branche
   - **Local Git** : Utiliser git push
   - **Azure CLI** : Utiliser `az webapp up`
3. Sauvegarder

### Étape 3 : Configuration

1. **Configuration** → **General settings** → **Startup Command** :
   ```
   startup.sh
   ```

2. **Configuration** → **Application settings** → Ajouter :
   ```
   ALLOWED_ORIGINS = https://your-frontend.vercel.app
   GUNICORN_WORKERS = 2
   GUNICORN_TIMEOUT = 120
   ```

3. **Configuration** → **Path mappings** (si nécessaire pour les fichiers statiques)

### Étape 4 : Déployer le code

#### Via GitHub Actions (automatique)

Le Deployment Center créera automatiquement un workflow GitHub Actions.

#### Via Git Local

```bash
cd backend

# Ajouter le remote Azure
az webapp deployment source config-local-git \
  --name my-content-api \
  --resource-group my-content-rg

# Récupérer l'URL Git
git remote add azure https://my-content-api.scm.azurewebsites.net/my-content-api.git

# Déployer
git push azure main
```

## Option 3 : Déploiement avec Docker (Container)

Si vous préférez utiliser le Dockerfile créé :

### Étape 1 : Build et push l'image

```bash
cd backend

# Se connecter à Azure Container Registry
az acr create \
  --resource-group my-content-rg \
  --name mycontentregistry \
  --sku Basic

az acr login --name mycontentregistry

# Build et push
docker build -t mycontentregistry.azurecr.io/my-content-api:latest .
docker push mycontentregistry.azurecr.io/my-content-api:latest
```

### Étape 2 : Créer Web App for Containers

```bash
az webapp create \
  --name my-content-api \
  --resource-group my-content-rg \
  --plan my-content-plan \
  --deployment-container-image-name mycontentregistry.azurecr.io/my-content-api:latest

# Configurer le registry
az webapp config container set \
  --name my-content-api \
  --resource-group my-content-rg \
  --docker-registry-server-url https://mycontentregistry.azurecr.io \
  --docker-registry-server-user mycontentregistry \
  --docker-registry-server-password $(az acr credential show --name mycontentregistry --query "passwords[0].value" -o tsv)
```

## Mise à jour de l'application

### Redéploiement automatique

```bash
# Si vous avez utilisé az webapp up, relancez simplement :
cd backend
az webapp up --name my-content-api --resource-group my-content-rg
```

### Redéploiement manuel

```bash
# Via Git
git push azure main

# Via Azure CLI (zip deploy)
cd backend
zip -r app.zip . -x "*.git*" "__pycache__/*" "*.pyc" "venv/*"
az webapp deployment source config-zip \
  --name my-content-api \
  --resource-group my-content-rg \
  --src app.zip
```

## Gestion des fichiers volumineux (Git LFS)

Les embeddings (348MB) utilisent Git LFS. Azure App Service supporte Git LFS :

```bash
# Vérifier que Git LFS est bien configuré
git lfs ls-files

# Si besoin, installer Git LFS
git lfs install
git lfs track "*.pickle"
git lfs track "*.pkl"
git add .gitattributes
git commit -m "Configure Git LFS"
```

Azure téléchargera automatiquement les fichiers Git LFS lors du déploiement.

## Monitoring et debugging

### Voir les logs en temps réel

**Méthode 1 : Streaming en temps réel via CLI** (recommandé)

```bash
# Voir les logs en continu (comme tail -f)
az webapp log tail \
  --name my-content-api-oc \
  --resource-group my-content-rg

# Appuyez sur Ctrl+C pour arrêter le streaming
```

**Méthode 2 : Télécharger tous les logs**

```bash
# Télécharger un zip avec tous les logs
az webapp log download \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --log-file azure-logs.zip

# Extraire et consulter
unzip azure-logs.zip -d logs/
tail -100 logs/LogFiles/Application/*.log
```

**Méthode 3 : Consulter les logs récents**

```bash
# Télécharger et afficher les 100 dernières lignes
az webapp log download \
  --name my-content-api-oc \
  --resource-group my-content-rg \
  --log-file /tmp/logs.zip && \
  unzip -q /tmp/logs.zip -d /tmp/logs && \
  tail -100 /tmp/logs/LogFiles/Application/*.log
```

### Via le portail Azure

1. Aller sur https://portal.azure.com
2. Rechercher **my-content-api-oc**
3. **Monitoring** → **Log stream** (streaming en temps réel)
4. **Diagnose and solve problems** → troubleshooting automatique
5. **Logs** → télécharger les fichiers de logs

### Application Insights (recommandé pour production)

```bash
# Créer Application Insights
az monitor app-insights component create \
  --app my-content-insights \
  --location westeurope \
  --resource-group my-content-rg

# Lier à l'App Service
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app my-content-insights \
  --resource-group my-content-rg \
  --query instrumentationKey -o tsv)

az webapp config appsettings set \
  --name my-content-api \
  --resource-group my-content-rg \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="InstrumentationKey=$INSTRUMENTATION_KEY"
```

## Sécurité

### Restreindre les origines CORS

```bash
# Mettre à jour ALLOWED_ORIGINS avec vos vrais domaines
az webapp config appsettings set \
  --name my-content-api \
  --resource-group my-content-rg \
  --settings ALLOWED_ORIGINS="https://my-content-frontend.vercel.app,https://yourdomain.com"
```

### Activer HTTPS uniquement

```bash
az webapp update \
  --name my-content-api \
  --resource-group my-content-rg \
  --https-only true
```

### Configurer un domaine personnalisé (optionnel)

```bash
# Mapper un domaine personnalisé
az webapp config hostname add \
  --webapp-name my-content-api \
  --resource-group my-content-rg \
  --hostname api.yourdomain.com

# Activer SSL managed certificate (gratuit)
az webapp config ssl bind \
  --name my-content-api \
  --resource-group my-content-rg \
  --certificate-thumbprint <thumbprint> \
  --ssl-type SNI
```

## Coûts estimés

### Plan Basic B1 (~13€/mois) ❌ Non recommandé
- 1 core, 1.75 GB RAM
- 10 GB stockage
- **Problème** : RAM insuffisante pour les embeddings (348MB)
- Workers Gunicorn killed par OOM (Out Of Memory)
- ⚠️ Utilisable avec 1 worker uniquement (performances très limitées)

### Plan Standard S1 (~60€/mois) ✅ Recommandé
- 1 core, 1.75 GB RAM
- 50 GB stockage
- **Déployé en production** : `https://my-content-api-oc.azurewebsites.net`
- Fonctionne correctement avec 2 workers Gunicorn
- Staging slots, autoscaling
- Idéal pour production avec trafic modéré

### Plan Premium P1V2 (~150€/mois) 🚀 Optimal
- 1 core, 3.5 GB RAM
- 250 GB stockage
- Meilleures performances
- Recommandé pour production avec trafic élevé
- Plus de marge pour les pics de charge

## Troubleshooting

### ⚠️ Workers Gunicorn tués (SIGKILL / Out of Memory)

**Symptôme** : Dans les logs, vous voyez :
```
[ERROR] Worker (pid:1022) was sent SIGKILL! Perhaps out of memory?
```

**Cause** : Le plan B1 Basic (1.75GB RAM) est insuffisant pour charger les embeddings (348MB) avec plusieurs workers.

**Solutions** :
1. **Upgrader vers S1 Standard** (recommandé) :
   ```bash
   az appservice plan update --name <NOM_DU_PLAN> --resource-group my-content-rg --sku S1
   ```

2. **Ou réduire à 1 worker** (temporaire) :
   ```bash
   az webapp config appsettings set --name my-content-api-oc --resource-group my-content-rg --settings "GUNICORN_WORKERS=1"
   az webapp restart --name my-content-api-oc --resource-group my-content-rg
   ```

### Premier appel très lent (20-60 secondes)

**Symptôme** : Le premier appel à `/health` ou aux endpoints utilisant les embeddings timeout ou prend très longtemps.

**Cause** : Chargement initial des 348MB d'embeddings en mémoire.

**Solution** : C'est normal. Après le premier appel, les données restent en cache et les réponses sont instantanées. Vous pouvez :
- Augmenter le timeout de votre client HTTP
- Précharger les données au démarrage (modification du code)
- Utiliser un plan plus puissant (P1V2) pour un chargement plus rapide

### L'application ne démarre pas

```bash
# Vérifier les logs
az webapp log tail --name my-content-api --resource-group my-content-rg

# Vérifier le startup command
az webapp config show \
  --name my-content-api \
  --resource-group my-content-rg \
  --query "appCommandLine"
```

### Erreur "Module not found"

Vérifier que `requirements.txt` est bien présent et que le build s'est exécuté :

```bash
az webapp config appsettings set \
  --name my-content-api \
  --resource-group my-content-rg \
  --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### Problème avec les embeddings (fichiers volumineux)

Vérifier que Git LFS est activé et que les fichiers sont bien trackés :

```bash
git lfs ls-files
git lfs pull
```

### Timeout sur les requêtes

Augmenter le timeout Gunicorn :

```bash
az webapp config appsettings set \
  --name my-content-api \
  --resource-group my-content-rg \
  --settings GUNICORN_TIMEOUT=300
```

## Ressources utiles

- [Documentation Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/)
- [Python sur App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [FastAPI sur Azure](https://learn.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app-fastapi)
- [Tarification App Service](https://azure.microsoft.com/en-us/pricing/details/app-service/linux/)

## Support

Pour toute question, consultez :
- Documentation du projet : `CLAUDE.md`
- GitHub Issues : [lien vers votre repo]
- Documentation Azure : https://learn.microsoft.com/en-us/azure/app-service/
