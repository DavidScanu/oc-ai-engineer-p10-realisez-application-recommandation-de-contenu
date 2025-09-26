# backend/recommenders/content.py
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from .base import BaseRecommender

logger = logging.getLogger(__name__)

class ContentRecommender(BaseRecommender):
    """Recommandeur basé sur la similarité de contenu"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader)
        self._similarity_cache = {}
    
    def recommend(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Recommande des articles similaires à ceux consultés par l'utilisateur"""
        logger.info(f"📖 Recommandation par contenu pour user {user_id}")
        
        # Récupérer l'historique utilisateur
        user_history = self.data_loader.get_user_history(user_id, limit=10)  # 10 derniers articles
        
        if len(user_history) == 0:
            logger.warning(f"⚠️ Aucun historique pour user {user_id}, fallback sur popularité")
            # Fallback sur popularité pour nouveaux utilisateurs
            from .popularity import PopularityRecommender
            fallback = PopularityRecommender(self.data_loader)
            return fallback.recommend(user_id, n_recommendations, **kwargs)
        
        # Charger les embeddings et métadonnées
        embeddings = self.data_loader.load_articles_embeddings()
        metadata = self.data_loader.load_articles_metadata()
        available_articles = self._get_available_articles(user_id, kwargs.get('exclude_seen', True))
        
        if len(available_articles) == 0:
            logger.warning(f"⚠️ Aucun article disponible pour user {user_id}")
            return []
        
        # Calculer le profil utilisateur (moyenne des embeddings des articles vus)
        user_articles = user_history['click_article_id'].tolist()
        user_embeddings = []
        
        for article_id in user_articles:
            if article_id < len(embeddings):  # Vérifier que l'ID est valide
                user_embeddings.append(embeddings[article_id])
        
        if len(user_embeddings) == 0:
            logger.warning(f"⚠️ Aucun embedding trouvé pour les articles de user {user_id}")
            return []
        
        # Profil utilisateur = moyenne des embeddings
        user_profile = np.mean(user_embeddings, axis=0).reshape(1, -1)
        
        # Calculer similarités avec tous les articles disponibles (vectorisé)
        article_ids = available_articles['article_id'].tolist()
        category_ids = available_articles['category_id'].tolist()

        # Filtrer les IDs valides et préparer les embeddings
        valid_data = []
        article_embeddings_list = []

        for i, article_id in enumerate(article_ids):
            if article_id < len(embeddings):
                valid_data.append({
                    'article_id': article_id,
                    'category_id': category_ids[i]
                })
                article_embeddings_list.append(embeddings[article_id])

        if len(article_embeddings_list) == 0:
            logger.warning(f"⚠️ Aucun embedding valide trouvé pour les articles disponibles")
            return []

        # Calcul vectorisé des similarités
        article_embeddings_matrix = np.array(article_embeddings_list)
        similarities_scores = cosine_similarity(user_profile, article_embeddings_matrix)[0]

        # Créer la liste des similarités
        similarities = []
        for i, data in enumerate(valid_data):
            similarities.append({
                'article_id': data['article_id'],
                'similarity': similarities_scores[i],
                'category_id': data['category_id']
            })
        
        # Trier par similarité
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Générer les recommandations
        recommendations = []
        for i, item in enumerate(similarities[:n_recommendations]):
            reason = f"Similaire à vos lectures (score: {item['similarity']:.3f})"
            
            recommendations.append(self._format_recommendation(
                article_id=item['article_id'],
                score=item['similarity'],
                reason=reason
            ))
        
        logger.info(f"📖 {len(recommendations)} recommandations par contenu générées")
        return recommendations