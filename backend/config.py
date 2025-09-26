# backend/config.py
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
from datetime import datetime

class Settings(BaseSettings):
    # Chemins
    DATA_PATH: Path = Path("data")  # Relatif à backend/
    
    # Paramètres temporels (auto-adaptés aux données)
    POPULARITY_WINDOW_DAYS: int = 90  # 90 jours pour la popularité
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
    
    # Seuil pour nouveaux utilisateurs
    MIN_USER_INTERACTIONS: int = 3
    
    # Fréquence de mise à jour des clusters (en heures)
    CLUSTER_UPDATE_FREQUENCY_HOURS: int = 24
    
    # Date de référence (auto-détectée si None)
    REFERENCE_DATE: Optional[datetime] = None
    
    class Config:
        env_file = ".env"

settings = Settings()