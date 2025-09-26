# backend/recommenders/popularity.py
from typing import List, Dict, Any
import pandas as pd
import logging
from .base import BaseRecommender

logger = logging.getLogger(__name__)

class PopularityRecommender(BaseRecommender):
    """Recommandeur basé sur la popularité récente"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader)
        self._popular_articles_cache = None
        self._cache_timestamp = None
    
    def recommend(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Recommande les articles les plus populaires récemment"""
        logger.info(f"🔥 Recommandation par popularité pour user {user_id}")
        
        # Récupérer les articles populaires
        popular_articles = self.data_loader.get_recent_popular_articles()
        
        if len(popular_articles) == 0:
            logger.warning(f"⚠️ Aucun article populaire trouvé")
            return []
        
        # Exclure les articles déjà vus si demandé
        exclude_seen = kwargs.get('exclude_seen', True)
        if exclude_seen:
            seen_articles = self._get_user_seen_articles(user_id)
            available_articles = popular_articles[~popular_articles.index.isin(seen_articles)]
            logger.debug(f"👤 User {user_id}: {len(popular_articles)} populaires → {len(available_articles)} non vus")
        else:
            available_articles = popular_articles
        
        # Prendre le top N
        recommendations = []
        for i, (article_id, row) in enumerate(available_articles.head(n_recommendations).iterrows()):
            score = row['popularity_score']
            reason = f"Article populaire (#{i+1}) - {row['unique_users']} utilisateurs, {row['total_clicks']} clics"
            
            recommendations.append(self._format_recommendation(
                article_id=article_id,
                score=score,
                reason=reason
            ))
        
        logger.info(f"🔥 {len(recommendations)} recommandations par popularité générées")
        return recommendations