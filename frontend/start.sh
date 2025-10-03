#!/bin/bash

# Script de démarrage du frontend My Content

echo "🚀 Démarrage du frontend My Content..."
echo ""

# Vérifier si .env.local existe
if [ ! -f .env.local ]; then
    echo "⚠️  Fichier .env.local non trouvé. Copie de .env.example..."
    cp .env.example .env.local
    echo "✅ Fichier .env.local créé. Modifiez-le si nécessaire."
    echo ""
fi

# Vérifier si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 Installation des dépendances..."
    npm install
    echo ""
fi

# Démarrer le serveur de développement
echo "🌐 Démarrage du serveur de développement..."
echo "   L'application sera accessible sur http://localhost:3000"
echo ""
npm run dev
