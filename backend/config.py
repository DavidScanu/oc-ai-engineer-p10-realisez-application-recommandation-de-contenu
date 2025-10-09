# backend/config.py
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
from datetime import datetime

class Settings(BaseSettings):
    # Chemins
    DATA_PATH: Path = Path("data")  # Relatif à backend/
    
    # Paramètres temporels (auto-adaptés aux données)
    MAX_ARTICLE_AGE_DAYS: int = 730   # 2 ans pour les articles recommandables
    MIN_WORDS_COUNT: int = 50         # Filtrage articles courts
    
    # Paramètres de recommandation
    N_RECOMMENDATIONS: int = 5
    N_USER_CLUSTERS: int = 5
    
    # Poids pour l'approche hybride
    HYBRID_WEIGHTS: dict = {
        "clustering": 0.4,
        "content": 0.3,
        "popularity": 0.2,
        "diversity": 0.1
    }
    
    # Seuil pour nouveaux utilisateurs (cold start)
    # Nombre minimum d'articles uniques lus (pas le nombre total de clics)
    # Valeurs recommandées : 3 (permissif), 5 (équilibré), 10 (conservateur)
    MIN_UNIQUE_ARTICLES_READ: int = 5
    
    # Fréquence de mise à jour des clusters (en heures)
    CLUSTER_UPDATE_FREQUENCY_HOURS: int = 24

    # Solution 1: Boost temporaire de nouveauté (cold start nouveaux articles)
    NOVELTY_BOOST_24H: float = 1.5   # +50% de score pour articles < 24h
    NOVELTY_BOOST_72H: float = 1.2   # +20% de score pour articles 24-72h

    # Solution 2: Recommandations "Articles récents" dédiées
    RECENT_ARTICLES_CUTOFF_HOURS: int = 48  # Fenêtre par défaut pour articles récents

    # Date de référence (auto-détectée si None)
    REFERENCE_DATE: Optional[datetime] = None

    class Config:
        # Variables d'environnement peuvent surcharger ces valeurs
        # Créez un fichier .env (voir .env.example) pour personnaliser
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()