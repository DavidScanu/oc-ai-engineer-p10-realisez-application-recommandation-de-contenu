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
        return len(user_history) < settings.MIN_USER_INTERACTIONS
    
    def _get_available_articles(self, user_id: int, exclude_seen: bool = True) -> pd.DataFrame:
        """Récupère les articles disponibles pour recommandation"""
        recommendable = self.data_loader.get_recommendable_articles()
        
        if exclude_seen:
            seen_articles = self._get_user_seen_articles(user_id)
            available = recommendable[~recommendable['article_id'].isin(seen_articles)]
            logger.debug(f"👤 User {user_id}: {len(recommendable)} articles → {len(available)} non vus")
            return available
        
        return recommendable