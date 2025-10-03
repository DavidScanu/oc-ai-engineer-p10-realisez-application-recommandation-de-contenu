# Guide de dépannage - Frontend My Content

## 🔧 Problèmes courants et solutions

### 1. Erreur de connexion au backend

**Symptôme** : Message d'erreur dans l'interface "Erreur: [message]"

**Solutions** :

```bash
# 1. Vérifier que le backend est démarré
curl http://localhost:8000/health

# Si pas de réponse, démarrer le backend :
cd ../backend
./start.sh
# ou
uvicorn main:app --reload

# 2. Vérifier la variable d'environnement
cat frontend/.env.local
# Doit contenir : NEXT_PUBLIC_API_URL=http://localhost:8000

# 3. Vérifier les CORS
# Le backend doit avoir CORS activé pour localhost:3000
```

### 2. Page blanche / Erreur React

**Symptôme** : Page complètement blanche ou erreur dans la console

**Solutions** :

```bash
# 1. Effacer le cache Next.js
rm -rf .next
npm run dev

# 2. Réinstaller les dépendances
rm -rf node_modules package-lock.json
npm install

# 3. Vérifier la version de Node.js
node --version  # Doit être >= 20.x
```

### 3. Styles Tailwind ne s'appliquent pas

**Symptôme** : Interface sans styles ou mal stylée

**Solutions** :

```bash
# 1. Vérifier que globals.css est importé
# Doit être dans app/layout.tsx

# 2. Redémarrer le serveur
npm run dev

# 3. Vérifier la configuration Tailwind
cat postcss.config.mjs
```

### 4. Erreur "[object Object]" dans la console

**Symptôme** : Erreur peu descriptive dans la console

**Solutions** :

Cette erreur a été corrigée avec une meilleure gestion d'erreur. Si elle persiste :

```bash
# 1. Mettre à jour le code
git pull

# 2. Vérifier lib/api.ts ligne 21-45
# Doit contenir le try-catch amélioré

# 3. Vérifier que le backend retourne des erreurs JSON valides
```

### 5. TypeScript / ESLint errors

**Symptôme** : Erreurs lors du build

**Solutions** :

```bash
# 1. Vérifier les types
npm run build

# 2. Fix ESLint
npm run lint

# 3. Si erreurs persistent, vérifier tsconfig.json
cat tsconfig.json
```

### 6. Module not found errors

**Symptôme** : Cannot find module '@/...'

**Solutions** :

```bash
# 1. Vérifier que le chemin alias est configuré
# Dans tsconfig.json, doit avoir:
# "paths": { "@/*": ["./*"] }

# 2. Redémarrer le serveur TypeScript
# VS Code: Ctrl+Shift+P > "TypeScript: Restart TS Server"

# 3. Réinstaller
rm -rf node_modules .next
npm install
```

### 7. Build lent ou timeouts

**Symptôme** : `npm run build` prend trop de temps

**Solutions** :

```bash
# 1. Désactiver Turbopack temporairement
next build  # Au lieu de next build --turbopack

# 2. Vérifier l'espace disque
df -h

# 3. Nettoyer le cache
rm -rf .next node_modules/.cache
```

### 8. Recommandations ne se chargent pas

**Symptôme** : Spinner infini ou pas de recommandations

**Vérifications** :

```bash
# 1. Backend fonctionne ?
curl -X POST "http://localhost:8000/recommend/5890?method=hybrid&n_recommendations=5"

# 2. L'utilisateur existe ?
curl http://localhost:8000/users/5890/stats

# 3. Console browser (F12)
# Vérifier les erreurs réseau
```

### 9. Port 3000 déjà utilisé

**Symptôme** : Error: listen EADDRINUSE :::3000

**Solutions** :

```bash
# 1. Utiliser un autre port
PORT=3001 npm run dev

# 2. Ou tuer le processus existant
lsof -ti:3000 | xargs kill -9

# 3. Puis redémarrer
npm run dev
```

### 10. Vercel deployment fails

**Symptôme** : Erreur lors du déploiement Vercel

**Solutions** :

```bash
# 1. Vérifier le build local
npm run build
npm start

# 2. Configurer les variables d'environnement sur Vercel
# NEXT_PUBLIC_API_URL=https://votre-backend.azurewebsites.net

# 3. Vérifier les logs Vercel
vercel logs [deployment-url]
```

## 🔍 Debugging avancé

### Activer les logs détaillés

```bash
# Mode debug Next.js
DEBUG=* npm run dev

# Logs réseau dans le browser
# F12 > Network tab > Cocher "Preserve log"
```

### Vérifier l'état de l'application

```bash
# 1. Santé du backend
curl http://localhost:8000/health | jq

# 2. Test d'un endpoint
curl -X POST "http://localhost:8000/recommend/5890?method=hybrid" | jq

# 3. CORS headers
curl -I -X OPTIONS http://localhost:8000/recommend/5890
```

### Tester les composants isolément

```typescript
// Dans app/page.tsx, temporairement simplifier :
export default function HomePage() {
  return <div>Test</div>;
}
// Si ça fonctionne, le problème vient des composants
```

## 📞 Support

Si aucune solution ne fonctionne :

1. **Vérifier les issues GitHub** : Problème déjà connu ?
2. **Consulter les logs** : `npm run dev` affiche les erreurs détaillées
3. **Version minimal** : Créer une page de test minimale
4. **Réinitialiser** :
   ```bash
   rm -rf node_modules .next
   npm install
   npm run dev
   ```

## ✅ Checklist rapide

Avant de débugger, vérifier :

- [ ] Backend démarré (`curl http://localhost:8000/health`)
- [ ] `.env.local` configuré correctement
- [ ] Node.js >= 20.x (`node --version`)
- [ ] Dépendances installées (`npm list`)
- [ ] Port 3000 libre (`lsof -i :3000`)
- [ ] Console browser sans erreurs (F12)
- [ ] Cache Next.js vidé (`rm -rf .next`)

---

**Dernière mise à jour** : 2025-10-03
