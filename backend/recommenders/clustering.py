# backend/recommenders/clustering.py
from typing import List, Dict, Any
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import logging
import pickle
import os
from datetime import datetime, timedelta
from .base import BaseRecommender

logger = logging.getLogger(__name__)

class ClusteringRecommender(BaseRecommender):
    """Recommandeur basé sur la segmentation d'utilisateurs"""
    
    def __init__(self, data_loader):
        super().__init__(data_loader)
        self._user_clusters = None
        self._cluster_model = None
        self._scaler = None
        self._last_training = None
        self._cluster_characteristics = None
        self._clusters_file_path = "data/clusters_cache.pkl"

        # Charger les clusters sauvegardés au démarrage
        self._load_clusters()
    
    def _should_retrain_clusters(self) -> bool:
        """Vérifie si les clusters doivent être recalculés"""
        from config import settings
        
        if self._last_training is None:
            return True
        
        hours_since_training = (datetime.now() - self._last_training).total_seconds() / 3600
        return hours_since_training >= settings.CLUSTER_UPDATE_FREQUENCY_HOURS

    def _save_clusters(self):
        """Sauvegarde les clusters sur disque"""
        if self._user_clusters is None:
            return

        try:
            # Créer le répertoire si nécessaire
            os.makedirs(os.path.dirname(self._clusters_file_path), exist_ok=True)

            # Données à sauvegarder
            clusters_data = {
                'user_clusters': self._user_clusters,
                'cluster_model': self._cluster_model,
                'scaler': self._scaler,
                'last_training': self._last_training,
                'cluster_characteristics': self._cluster_characteristics
            }

            with open(self._clusters_file_path, 'wb') as f:
                pickle.dump(clusters_data, f)

            logger.info(f"💾 Clusters sauvegardés dans {self._clusters_file_path}")

        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde des clusters: {e}")

    def _load_clusters(self):
        """Charge les clusters depuis le disque"""
        if not os.path.exists(self._clusters_file_path):
            logger.info("📁 Aucun fichier de clusters trouvé, démarrage à froid")
            return

        try:
            with open(self._clusters_file_path, 'rb') as f:
                clusters_data = pickle.load(f)

            self._user_clusters = clusters_data.get('user_clusters')
            self._cluster_model = clusters_data.get('cluster_model')
            self._scaler = clusters_data.get('scaler')
            self._last_training = clusters_data.get('last_training')
            self._cluster_characteristics = clusters_data.get('cluster_characteristics')

            logger.info(f"📁 Clusters chargés depuis {self._clusters_file_path}")
            if self._last_training:
                logger.info(f"📅 Dernier entraînement: {self._last_training}")

        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement des clusters: {e}")
            # Réinitialiser en cas d'erreur
            self._user_clusters = None
            self._cluster_model = None
            self._scaler = None
            self._last_training = None
            self._cluster_characteristics = None
    
    def _build_user_features(self) -> pd.DataFrame:
        """Construit les features des utilisateurs pour le clustering"""
        logger.info("🔨 Construction des features utilisateurs")
        
        interactions = self.data_loader.load_user_interactions()
        metadata = self.data_loader.load_articles_metadata()
        
        # Merger interactions avec métadonnées
        merged = interactions.merge(
            metadata[['article_id', 'category_id', 'words_count']], 
            left_on='click_article_id', 
            right_on='article_id', 
            how='left'
        )
        
        # Features par utilisateur
        user_features = merged.groupby('user_id').agg({
            'click_article_id': ['count', 'nunique'],  # Nombre total de clics et d'articles uniques
            'category_id': lambda x: x.nunique(),      # Diversité des catégories
            'words_count': ['mean', 'std'],            # Préférences de longueur d'articles
            'click_timestamp': ['min', 'max']          # Période d'activité
        }).fillna(0)
        
        # Aplatir les colonnes multi-niveaux
        user_features.columns = [
            'total_clicks', 'unique_articles', 'category_diversity',
            'avg_words', 'std_words', 'first_interaction', 'last_interaction'
        ]
        
        # Features temporelles
        user_features['activity_span_hours'] = (
            user_features['last_interaction'] - user_features['first_interaction']
        ) / (1000 * 3600)  # Conversion ms vers heures
        
        user_features['clicks_per_hour'] = user_features['total_clicks'] / (
            user_features['activity_span_hours'] + 1
        )  # +1 pour éviter division par 0
        
        # Features de préférences par catégories (top 10 catégories)
        top_categories = merged['category_id'].value_counts().head(10).index
        
        for cat_id in top_categories:
            cat_clicks = merged[merged['category_id'] == cat_id].groupby('user_id')['click_article_id'].count()
            user_features[f'cat_{cat_id}_clicks'] = cat_clicks.fillna(0)
            user_features[f'cat_{cat_id}_ratio'] = user_features[f'cat_{cat_id}_clicks'] / user_features['total_clicks']
        
        # Nettoyer les features
        user_features = user_features.fillna(0)
        user_features = user_features.replace([np.inf, -np.inf], 0)
        
        logger.info(f"🔨 Features construites: {len(user_features)} utilisateurs, {len(user_features.columns)} features")
        return user_features
    
    def _train_clusters(self):
        """Entraîne le modèle de clustering"""
        from config import settings
        
        logger.info(f"🧠 Entraînement du clustering ({settings.N_USER_CLUSTERS} clusters)")
        
        # Construire les features
        user_features = self._build_user_features()
        
        if len(user_features) == 0:
            logger.error("❌ Aucune feature utilisateur disponible")
            return
        
        # Normalisation
        self._scaler = StandardScaler()
        features_scaled = self._scaler.fit_transform(user_features.values)
        
        # Clustering K-means
        self._cluster_model = KMeans(
            n_clusters=settings.N_USER_CLUSTERS, 
            random_state=42,
            n_init=10
        )
        
        cluster_labels = self._cluster_model.fit_predict(features_scaled)
        
        # Sauvegarder les assignations
        self._user_clusters = pd.DataFrame({
            'user_id': user_features.index,
            'cluster': cluster_labels
        }).set_index('user_id')
        
        # Calculer les caractéristiques des clusters
        self._cluster_characteristics = {}
        for cluster_id in range(settings.N_USER_CLUSTERS):
            cluster_users = user_features[cluster_labels == cluster_id]
            
            self._cluster_characteristics[cluster_id] = {
                'size': len(cluster_users),
                'avg_clicks': cluster_users['total_clicks'].mean(),
                'avg_diversity': cluster_users['category_diversity'].mean(),
                'avg_words_preference': cluster_users['avg_words'].mean(),
                'activity_level': cluster_users['clicks_per_hour'].mean()
            }
        
        self._last_training = datetime.now()
        logger.info(f"🧠 Clustering terminé: {len(self._user_clusters)} utilisateurs assignés")

        # Sauvegarder les clusters après entraînement
        self._save_clusters()
        
        # Log des caractéristiques
        for cluster_id, chars in self._cluster_characteristics.items():
            logger.info(f"📊 Cluster {cluster_id}: {chars['size']} users, "
                       f"{chars['avg_clicks']:.1f} clics moy., "
                       f"{chars['avg_diversity']:.1f} catégories moy.")
    
    def _get_user_cluster(self, user_id: int) -> int:
        """Récupère le cluster d'un utilisateur"""
        if self._should_retrain_clusters():
            self._train_clusters()
        
        if self._user_clusters is None or user_id not in self._user_clusters.index:
            # Utilisateur non trouvé, assigner au cluster le plus général
            logger.warning(f"⚠️ User {user_id} non trouvé dans les clusters, assignation au cluster 0")
            return 0
        
        return self._user_clusters.loc[user_id, 'cluster']
    
    def recommend(self, user_id: int, n_recommendations: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Recommande des articles populaires dans le cluster de l'utilisateur"""
        logger.info(f"👥 Recommandation par clustering pour user {user_id}")

        # Vérifier si l'utilisateur a suffisamment d'historique VALIDE
        if not self._has_sufficient_history(user_id):
            logger.warning(
                f"⚠️ User {user_id} : historique insuffisant ou invalide, "
                f"fallback vers popularité (cold start)"
            )
            # Fallback sur popularité pour nouveaux utilisateurs (cold start)
            from .popularity import PopularityRecommender
            fallback = PopularityRecommender(self.data_loader)
            recommendations = fallback.recommend(user_id, n_recommendations, **kwargs)
            # Marquer le fallback dans les métadonnées
            if recommendations and isinstance(recommendations, list):
                for rec in recommendations:
                    rec['fallback_from'] = 'clustering'
                    rec['fallback_reason'] = 'insufficient_valid_history'
            return recommendations

        # Récupérer le cluster de l'utilisateur
        user_cluster = self._get_user_cluster(user_id)
        logger.debug(f"👤 User {user_id} → Cluster {user_cluster}")

        if self._user_clusters is None:
            logger.error("❌ Clusters non disponibles")
            return []
        
        # Récupérer les utilisateurs du même cluster
        cluster_users = self._user_clusters[self._user_clusters['cluster'] == user_cluster].index.tolist()
        logger.debug(f"👥 Cluster {user_cluster}: {len(cluster_users)} utilisateurs")
        
        # Récupérer les interactions de ces utilisateurs
        interactions = self.data_loader.load_user_interactions()
        cluster_interactions = interactions[interactions['user_id'].isin(cluster_users)]
        
        if len(cluster_interactions) == 0:
            logger.warning(f"⚠️ Aucune interaction pour le cluster {user_cluster}")
            return []
        
        # Calculer la popularité des articles dans ce cluster
        article_popularity = cluster_interactions.groupby('click_article_id').agg({
            'user_id': 'nunique',
            'click_timestamp': 'count'
        }).rename(columns={
            'user_id': 'unique_users',
            'click_timestamp': 'total_clicks'
        })
        
        article_popularity['cluster_score'] = (
            0.6 * article_popularity['unique_users'] + 
            0.4 * article_popularity['total_clicks']
        )
        
        article_popularity = article_popularity.sort_values('cluster_score', ascending=False)
        
        # Exclure les articles déjà vus
        if kwargs.get('exclude_seen', True):
            seen_articles = self._get_user_seen_articles(user_id)
            available_articles = article_popularity[~article_popularity.index.isin(seen_articles)]
        else:
            available_articles = article_popularity
        
        # Vérifier que les articles sont recommandables (âge, qualité)
        recommendable_articles = self.data_loader.get_recommendable_articles()
        recommendable_ids = set(recommendable_articles['article_id'].tolist())
        available_articles = available_articles[available_articles.index.isin(recommendable_ids)]
        
        # Générer les recommandations
        recommendations = []
        cluster_chars = self._cluster_characteristics.get(user_cluster, {})
        
        for i, (article_id, row) in enumerate(available_articles.head(n_recommendations).iterrows()):
            reason = (f"Populaire dans votre segment (#{i+1}) - "
                     f"Cluster {user_cluster} ({cluster_chars.get('size', 0)} utilisateurs similaires)")
            
            recommendations.append(self._format_recommendation(
                article_id=article_id,
                score=row['cluster_score'],
                reason=reason
            ))
        
        logger.info(f"👥 {len(recommendations)} recommandations par clustering générées")
        return recommendations
    
    def get_user_segment_info(self, user_id: int) -> Dict:
        """Retourne les informations du segment de l'utilisateur"""
        cluster = self._get_user_cluster(user_id)
        characteristics = self._cluster_characteristics.get(cluster, {})

        return {
            "user_id": user_id,
            "segment": int(cluster),
            "segment_characteristics": characteristics,
            "confidence": 1.0  # Pour l'instant, confiance fixe
        }

    def force_retrain_clusters(self):
        """Force le recalcul des clusters (ignorer la fréquence configurée)"""
        logger.info("🔄 Recalcul forcé des clusters")
        self._last_training = None
        self._train_clusters()

    def clear_clusters_cache(self):
        """Supprime le fichier de cache des clusters"""
        if os.path.exists(self._clusters_file_path):
            try:
                os.remove(self._clusters_file_path)
                logger.info(f"🗑️ Cache des clusters supprimé: {self._clusters_file_path}")
            except Exception as e:
                logger.error(f"❌ Erreur lors de la suppression du cache: {e}")
        else:
            logger.info("📁 Aucun fichier de cache à supprimer")