# backend/recommenders/hybrid.py
from typing import List, Dict, Any
import pandas as pd
import numpy as np
import logging
from .base import BaseRecommender
from .popularity import PopularityRecommender
from .content import ContentRecommender
from .clustering import ClusteringRecommender

logger = logging.getLogger(__name__)

class HybridRecommender(BaseRecommender):
    """Recommandeur hybride combinant plusieurs approches"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader)
        self.popularity_rec = PopularityRecommender(data_loader)
        self.content_rec = ContentRecommender(data_loader)
        self.clustering_rec = ClusteringRecommender(data_loader)
    
    def recommend(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Combine les recommandations de plusieurs approches"""
        from config import settings
        
        logger.info(f"🎭 Recommandation hybride pour user {user_id}")
        
        # Paramètres
        weights = settings.HYBRID_WEIGHTS
        exclude_seen = kwargs.get('exclude_seen', True)
        
        # Collecter les recommandations de chaque approche
        all_recommendations = {}
        
        # 1. Clustering (40%)
        try:
            clustering_recs = self.clustering_rec.recommend(
                user_id, 
                n_recommendations=n_recommendations*2, 
                exclude_seen=exclude_seen
            )
            for rec in clustering_recs:
                article_id = rec['article_id']
                if article_id not in all_recommendations:
                    all_recommendations[article_id] = {
                        'article_id': article_id,
                        'scores': {},
                        'reasons': [],
                        'metadata': rec['metadata']
                    }
                all_recommendations[article_id]['scores']['clustering'] = rec['score']
                all_recommendations[article_id]['reasons'].append(f"Clustering: {rec['reason']}")
            
            logger.debug(f"🎭 Clustering: {len(clustering_recs)} recommandations")
        except Exception as e:
            logger.error(f"❌ Erreur clustering: {e}")
        
        # 2. Content-based (30%)
        try:
            content_recs = self.content_rec.recommend(
                user_id, 
                n_recommendations=n_recommendations*2, 
                exclude_seen=exclude_seen
            )
            for rec in content_recs:
                article_id = rec['article_id']
                if article_id not in all_recommendations:
                    all_recommendations[article_id] = {
                        'article_id': article_id,
                        'scores': {},
                        'reasons': [],
                        'metadata': rec['metadata']
                    }
                all_recommendations[article_id]['scores']['content'] = rec['score']
                all_recommendations[article_id]['reasons'].append(f"Contenu: {rec['reason']}")
            
            logger.debug(f"🎭 Content: {len(content_recs)} recommandations")
        except Exception as e:
            logger.error(f"❌ Erreur content: {e}")
        
        # 3. Popularity (20%)
        try:
            popularity_recs = self.popularity_rec.recommend(
                user_id, 
                n_recommendations=n_recommendations*2, 
                exclude_seen=exclude_seen
            )
            for rec in popularity_recs:
                article_id = rec['article_id']
                if article_id not in all_recommendations:
                    all_recommendations[article_id] = {
                        'article_id': article_id,
                        'scores': {},
                        'reasons': [],
                        'metadata': rec['metadata']
                    }
                all_recommendations[article_id]['scores']['popularity'] = rec['score']
                all_recommendations[article_id]['reasons'].append(f"Popularité: {rec['reason']}")
            
            logger.debug(f"🎭 Popularity: {len(popularity_recs)} recommandations")
        except Exception as e:
            logger.error(f"❌ Erreur popularity: {e}")
        
        # 4. Diversité (10%) - Bonus pour articles de catégories différentes
        try:
            user_history = self.data_loader.get_user_history(user_id, limit=20)
            if len(user_history) > 0:
                metadata = self.data_loader.load_articles_metadata()
                user_articles_with_cats = user_history.merge(
                    metadata[['article_id', 'category_id']], 
                    left_on='click_article_id', 
                    right_on='article_id', 
                    how='left'
                )
                
                if len(user_articles_with_cats) > 0:
                    user_categories = set(user_articles_with_cats['category_id'].dropna().tolist())
                    
                    # Bonus pour articles de nouvelles catégories
                    for article_id, rec_data in all_recommendations.items():
                        article_info = rec_data['metadata']
                        if article_info.get('category_id') not in user_categories:
                            all_recommendations[article_id]['scores']['diversity'] = 1.0
                            all_recommendations[article_id]['reasons'].append("Diversité: Nouvelle catégorie")
        except Exception as e:
            logger.error(f"❌ Erreur diversité: {e}")
        
        # Calculer les scores finaux
        final_recommendations = []
        for article_id, data in all_recommendations.items():
            scores = data['scores']
            
            # Score pondéré
            final_score = 0.0
            score_details = []
            
            for method, weight in weights.items():
                if method in scores:
                    # Normalisation des scores par méthode
                    if method == 'clustering':
                        normalized_score = min(scores[method] / 10.0, 1.0)  # Score clustering souvent > 1
                    elif method == 'content':
                        normalized_score = scores[method]  # Déjà entre 0 et 1
                    elif method == 'popularity':
                        normalized_score = min(scores[method] / 100.0, 1.0)  # Score popularité peut être élevé
                    else:  # diversity
                        normalized_score = scores[method]
                    
                    contribution = weight * normalized_score
                    final_score += contribution
                    score_details.append(f"{method}: {normalized_score:.3f} (×{weight})")
            
            # Bonus si l'article apparaît dans plusieurs méthodes
            methods_count = len(scores)
            if methods_count > 1:
                consensus_bonus = 0.1 * (methods_count - 1)
                final_score += consensus_bonus
                score_details.append(f"consensus: +{consensus_bonus:.3f}")
            
            reason = f"Score hybride: {final_score:.3f} ({', '.join(score_details)})"
            
            final_recommendations.append({
                'article_id': article_id,
                'score': final_score,
                'reason': reason,
                'methods_used': list(scores.keys()),
                'metadata': data['metadata']
            })
        
        # Trier par score final et prendre le top N
        final_recommendations.sort(key=lambda x: x['score'], reverse=True)
        final_recommendations = final_recommendations[:n_recommendations]
        
        logger.info(f"🎭 {len(final_recommendations)} recommandations hybrides générées")
        return final_recommendations