#!/bin/bash
# backend/start.sh

echo "🚀 Démarrage de My Content Recommender API"

# Vérifier que nous sommes dans le bon répertoire
if [ ! -f "main.py" ]; then
    echo "❌ Erreur: main.py non trouvé. Êtes-vous dans le dossier backend?"
    exit 1
fi

# Activer l'environnement virtuel Python s'il existe
if [ -d "venv" ]; then
    echo "🐍 Activation de l'environnement virtuel..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "🐍 Activation de l'environnement virtuel..."
    source .venv/bin/activate
fi

# Vérifier que les dépendances sont installées
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📦 Installation des dépendances..."
    pip3 install -r requirements.txt
fi

# Lancer l'API
echo "🎯 Lancement de l'API sur http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo "🔍 Santé API: http://localhost:8000/health"

uvicorn main:app --reload --host 0.0.0.0 --port 8000