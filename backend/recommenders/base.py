# backend/recommenders/base.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class BaseRecommender(ABC):
    """Classe de base pour tous les systèmes de recommandation"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.name = self.__class__.__name__
    
    @abstractmethod
    def recommend(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """
        Génère des recommandations pour un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            n_recommendations: Nombre de recommandations à retourner
            **kwargs: Paramètres additionnels
            
        Returns:
            Liste de dictionnaires contenant les recommandations
        """
        pass
    
    def _format_recommendation(self, article_id: int, score: float, reason: str = "") -> Dict[str, Any]:
        """Formate une recommandation"""
        article_info = self.data_loader.get_article_info(article_id)
        
        return {
            "article_id": int(article_id),
            "score": float(score),
            "reason": reason,
            "metadata": article_info
        }
    
    def _get_user_seen_articles(self, user_id: int) -> set:
        """Récupère les articles déjà vus par un utilisateur"""
        user_history = self.data_loader.get_user_history(user_id)
        return set(user_history['click_article_id'].tolist())
    
    def _is_new_user(self, user_id: int) -> bool:
        """Détermine si un utilisateur est nouveau (peu d'interactions)"""
        from config import settings
        user_history = self.data_loader.get_user_history(user_id)
        return len(user_history) < settings.MIN_UNIQUE_ARTICLES_READ
    
    def _get_available_articles(self, user_id: int, exclude_seen: bool = True) -> pd.DataFrame:
        """Récupère les articles disponibles pour recommandation"""
        recommendable = self.data_loader.get_recommendable_articles()

        if exclude_seen:
            seen_articles = self._get_user_seen_articles(user_id)
            available = recommendable[~recommendable['article_id'].isin(seen_articles)]
            logger.debug(f"👤 User {user_id}: {len(recommendable)} articles → {len(available)} non vus")
            return available

        return recommendable

    def _get_valid_user_article_ids(self, user_id: int) -> List[int]:
        """
        Récupère les article_id VALIDES de l'historique utilisateur.

        Valide = article_id existe dans les métadonnées

        Returns:
            Liste des article_id valides (peut être vide)
        """
        user_history = self.data_loader.get_user_history(user_id)

        if len(user_history) == 0:
            return []

        # Vérifier que les article_id existent dans les données
        metadata = self.data_loader.load_articles_metadata()
        valid_article_ids = set(metadata['article_id'].tolist())

        # Filtrer l'historique pour ne garder que les IDs valides
        valid_history = user_history[
            user_history['click_article_id'].isin(valid_article_ids)
        ]

        return valid_history['click_article_id'].tolist()

    def _has_sufficient_history(self, user_id: int) -> bool:
        """
        Vérifie si l'utilisateur a suffisamment d'historique VALIDE.

        Combine :
        - Quantité : >= MIN_UNIQUE_ARTICLES_READ (articles uniques lus)
        - Qualité : click_article_id valides uniquement

        Returns:
            True si suffisant, False si fallback nécessaire
        """
        from config import settings

        valid_articles = self._get_valid_user_article_ids(user_id)
        has_enough = len(valid_articles) >= settings.MIN_UNIQUE_ARTICLES_READ

        if not has_enough:
            logger.info(
                f"User {user_id}: insufficient valid history "
                f"({len(valid_articles)} unique articles read, "
                f"minimum: {settings.MIN_UNIQUE_ARTICLES_READ})"
            )

        return has_enough