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

    def _get_user_top_categories(self, user_id: int, top_n: int = 3) -> List[int]:
        """
        Solution 3: Récupère les top N catégories préférées de l'utilisateur

        Args:
            user_id: ID de l'utilisateur
            top_n: Nombre de catégories à retourner

        Returns:
            Liste des category_id préférés
        """
        user_history = self.data_loader.get_user_history(user_id)

        if len(user_history) == 0:
            return []

        # Joindre avec les métadonnées pour obtenir les catégories
        metadata = self.data_loader.load_articles_metadata()
        merged = user_history.merge(
            metadata[['article_id', 'category_id']],
            left_on='click_article_id',
            right_on='article_id',
            how='left'
        )

        if len(merged) == 0:
            return []

        # Compter les catégories
        category_counts = merged['category_id'].value_counts().head(top_n)

        return category_counts.index.tolist()

    def _get_user_avg_words_preference(self, user_id: int) -> float:
        """
        Solution 3: Calcule la longueur moyenne d'articles préférée par l'utilisateur

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Nombre moyen de mots des articles lus
        """
        user_history = self.data_loader.get_user_history(user_id)

        if len(user_history) == 0:
            return 0.0

        # Joindre avec les métadonnées pour obtenir words_count
        metadata = self.data_loader.load_articles_metadata()
        merged = user_history.merge(
            metadata[['article_id', 'words_count']],
            left_on='click_article_id',
            right_on='article_id',
            how='left'
        )

        if len(merged) == 0:
            return 0.0

        return merged['words_count'].mean()

    def _recommend_by_metadata(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """
        Solution 3: Recommandations par similarité de métadonnées (fallback sans embeddings)

        Utilisé lorsque les embeddings ne sont pas disponibles pour certains articles.
        Recommande des articles basés sur :
        - Les catégories préférées de l'utilisateur (top 3)
        - La longueur moyenne d'articles préférée (words_count)

        Args:
            user_id: ID de l'utilisateur
            n_recommendations: Nombre de recommandations

        Returns:
            Liste de recommandations basées sur les métadonnées
        """
        logger.info(f"📊 Recommandation par métadonnées pour user {user_id}")

        # Récupérer les préférences utilisateur
        top_categories = self._get_user_top_categories(user_id, top_n=3)
        avg_words = self._get_user_avg_words_preference(user_id)

        if len(top_categories) == 0:
            logger.warning(f"⚠️ Aucune catégorie trouvée pour user {user_id}, fallback vers popularité")
            from .popularity import PopularityRecommender
            fallback = PopularityRecommender(self.data_loader)
            return fallback.recommend(user_id, n_recommendations, **kwargs)

        # Récupérer les articles disponibles
        available_articles = self._get_available_articles(user_id, kwargs.get('exclude_seen', True))

        if len(available_articles) == 0:
            logger.warning(f"⚠️ Aucun article disponible pour user {user_id}")
            return []

        # Filtrer par catégories préférées
        candidates = available_articles[available_articles['category_id'].isin(top_categories)].copy()

        if len(candidates) == 0:
            logger.warning(f"⚠️ Aucun article dans les catégories préférées pour user {user_id}")
            # Fallback: prendre tous les articles disponibles
            candidates = available_articles.copy()

        # Scorer par similarité de longueur (si avg_words valide)
        if avg_words > 0:
            candidates['words_diff'] = abs(candidates['words_count'] - avg_words)
            candidates['metadata_score'] = 1.0 / (1.0 + candidates['words_diff'] / avg_words)
        else:
            candidates['metadata_score'] = 1.0

        # Bonus pour catégories préférées (top 1 = +0.3, top 2 = +0.2, top 3 = +0.1)
        for i, cat_id in enumerate(top_categories):
            bonus = 0.3 - (i * 0.1)
            candidates.loc[candidates['category_id'] == cat_id, 'metadata_score'] += bonus

        # Trier par score
        candidates = candidates.sort_values('metadata_score', ascending=False)

        # Générer les recommandations
        recommendations = []
        for i, row in enumerate(candidates.head(n_recommendations).itertuples()):
            reason = f"Catégorie préférée #{top_categories.index(row.category_id) + 1 if row.category_id in top_categories else '?'} (métadonnées)"

            recommendations.append(self._format_recommendation(
                article_id=row.article_id,
                score=row.metadata_score,
                reason=reason
            ))

        logger.info(f"📊 {len(recommendations)} recommandations par métadonnées générées")
        return recommendations
    
    def recommend(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Recommande des articles similaires à ceux consultés par l'utilisateur"""
        logger.info(f"📖 Recommandation par contenu pour user {user_id}")

        # Vérifier si l'utilisateur a suffisamment d'historique VALIDE
        if not self._has_sufficient_history(user_id):
            logger.warning(
                f"⚠️ User {user_id} : historique insuffisant ou invalide, "
                f"fallback vers popularité (cold start)"
            )
            # Fallback sur popularité pour nouveaux utilisateurs
            from .popularity import PopularityRecommender
            fallback = PopularityRecommender(self.data_loader)
            recommendations = fallback.recommend(user_id, n_recommendations, **kwargs)
            return recommendations
        
        # Charger les embeddings et métadonnées
        embeddings = self.data_loader.load_articles_embeddings()
        metadata = self.data_loader.load_articles_metadata()
        available_articles = self._get_available_articles(user_id, kwargs.get('exclude_seen', True))
        
        if len(available_articles) == 0:
            logger.warning(f"⚠️ Aucun article disponible pour user {user_id}")
            return []
        
        # Récupérer les article_id VALIDES de l'historique
        user_articles = self._get_valid_user_article_ids(user_id)

        # Double vérification (ne devrait jamais arriver grâce à _has_sufficient_history)
        if len(user_articles) == 0:
            logger.error(f"⚠️ User {user_id} : aucun article valide trouvé (cas anormal)")
            return []

        # Calculer les embeddings pour ces articles
        user_embeddings = []

        for article_id in user_articles:
            if article_id < len(embeddings):  # Sécurité supplémentaire
                user_embeddings.append(embeddings[article_id])

        # Cette condition ne devrait plus être nécessaire, mais on la garde par sécurité
        if len(user_embeddings) == 0:
            logger.error(f"⚠️ Aucun embedding trouvé pour user {user_id} (cas anormal)")
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