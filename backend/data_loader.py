# backend/data_loader.py
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
import glob
from typing import Dict, List, Set, Optional
from datetime import datetime, timedelta
import logging
from config import settings

logger = logging.getLogger(__name__)

class DataLoader:
    """Gestionnaire centralisé des données avec gestion temporelle adaptative"""
    
    def __init__(self):
        self.data_path = settings.DATA_PATH
        self._articles_metadata = None
        self._articles_embeddings = None
        self._user_interactions = None
        self._user_clusters = None
        self._cluster_update_time = None
        self._reference_date = None
        self._recommendable_articles = None
        
    def _get_reference_date(self) -> datetime:
        """Détecte automatiquement la date de référence (date max des données)"""
        if self._reference_date is None:
            if settings.REFERENCE_DATE:
                self._reference_date = settings.REFERENCE_DATE
            else:
                # Auto-détection depuis les données
                interactions = self.load_user_interactions()
                if len(interactions) > 0:
                    max_timestamp = interactions['click_timestamp'].max()
                    self._reference_date = datetime.fromtimestamp(max_timestamp / 1000)
                    logger.info(f"🕐 Date de référence auto-détectée: {self._reference_date.strftime('%Y-%m-%d')}")
                else:
                    self._reference_date = datetime.now()
                    logger.warning("⚠️ Utilisation de la date actuelle comme référence")
        
        return self._reference_date
    
    def load_articles_metadata(self) -> pd.DataFrame:
        """Charge les métadonnées des articles avec filtrage qualité"""
        if self._articles_metadata is None:
            metadata_path = self.data_path / "articles_metadata.csv"
            df = pd.read_csv(metadata_path)
            
            # Filtrage par nombre de mots
            before_filter = len(df)
            df = df[df['words_count'] >= settings.MIN_WORDS_COUNT].copy()
            after_filter = len(df)
            logger.info(f"📝 Filtrage articles courts: {before_filter:,} → {after_filter:,} articles ({before_filter-after_filter:,} supprimés)")
            
            # Ajout de la date de création
            df['created_date'] = pd.to_datetime(df['created_at_ts'], unit='ms')
            
            self._articles_metadata = df
            logger.info(f"📊 Métadonnées chargées: {len(df):,} articles")
            
        return self._articles_metadata
    
    def load_articles_embeddings(self) -> np.ndarray:
        """Charge les embeddings des articles"""
        if self._articles_embeddings is None:
            embeddings_path = self.data_path / "articles_embeddings.pickle"
            with open(embeddings_path, 'rb') as f:
                self._articles_embeddings = pickle.load(f)
            logger.info(f"🔢 Embeddings chargés: {self._articles_embeddings.shape}")
        return self._articles_embeddings
    
    def get_recommendable_articles(self) -> pd.DataFrame:
        """Récupère les articles recommandables (< 2 ans et > 50 mots)"""
        if self._recommendable_articles is None:
            metadata = self.load_articles_metadata()
            reference_date = self._get_reference_date()
            cutoff_date = reference_date - timedelta(days=settings.MAX_ARTICLE_AGE_DAYS)
            
            # Filtrage par âge
            recommendable = metadata[metadata['created_date'] >= cutoff_date].copy()
            
            logger.info(f"📅 Articles recommandables: {len(recommendable):,} (depuis {cutoff_date.strftime('%Y-%m-%d')})")
            self._recommendable_articles = recommendable
            
        return self._recommendable_articles
    
    def load_user_interactions(self, reload: bool = False) -> pd.DataFrame:
        """Charge toutes les interactions utilisateurs"""
        if self._user_interactions is None or reload:
            clicks_path = self.data_path / "clicks"
            click_files = glob.glob(str(clicks_path / "clicks_hour_*.csv"))
            
            dfs = []
            for file_path in click_files:
                try:
                    df = pd.read_csv(file_path)
                    dfs.append(df)
                except Exception as e:
                    logger.error(f"❌ Erreur {file_path}: {e}")
            
            if dfs:
                all_interactions = pd.concat(dfs, ignore_index=True)
                all_interactions['click_datetime'] = pd.to_datetime(
                    all_interactions['click_timestamp'], unit='ms'
                )
                
                # Filtrage des interactions sur articles recommandables uniquement après chargement
                # pour éviter la récursion lors de l'auto-détection de date
                if self._recommendable_articles is not None:
                    recommendable_ids = set(self._recommendable_articles['article_id'].tolist())
                    before_filter = len(all_interactions)
                    all_interactions = all_interactions[
                        all_interactions['click_article_id'].isin(recommendable_ids)
                    ]
                    after_filter = len(all_interactions)
                    logger.info(f"🔗 Interactions filtrées: {after_filter:,} (supprimées: {before_filter-after_filter:,})")
                
                self._user_interactions = all_interactions
                logger.info(f"🔗 Interactions chargées: {len(all_interactions):,}")
            else:
                self._user_interactions = pd.DataFrame()
                
        return self._user_interactions
    
    def get_user_history(self, user_id: int, limit: int = None) -> pd.DataFrame:
        """Récupère l'historique d'un utilisateur"""
        interactions = self.load_user_interactions()
        user_data = interactions[interactions['user_id'] == user_id].copy()
        user_data = user_data.sort_values('click_timestamp', ascending=False)
        
        if limit:
            user_data = user_data.head(limit)
            
        return user_data
    
    def get_recent_popular_articles(self, days: int = None) -> pd.DataFrame:
        """Récupère les articles populaires avec normalisation par âge de l'article"""
        interactions = self.load_user_interactions()
        metadata = self.load_articles_metadata()
        reference_date = self._get_reference_date()

        if len(interactions) == 0:
            logger.warning("⚠️ Aucune interaction disponible")
            return pd.DataFrame()

        # Agréger tous les clics par article
        popularity = interactions.groupby('click_article_id').agg({
            'user_id': 'nunique',
            'click_timestamp': 'count'
        }).rename(columns={
            'user_id': 'unique_users',
            'click_timestamp': 'total_clicks'
        })

        # Joindre avec les métadonnées pour obtenir la date de création
        popularity = popularity.merge(
            metadata[['article_id', 'created_date']],
            left_index=True,
            right_on='article_id',
            how='left'
        )

        # Calculer l'âge de l'article en mois
        popularity['article_age_days'] = (reference_date - popularity['created_date']).dt.days
        popularity['article_age_months'] = popularity['article_age_days'] / 30.0

        # Normaliser par l'âge (minimum 0.5 mois pour éviter division par zéro sur articles très récents)
        popularity['article_age_months'] = popularity['article_age_months'].clip(lower=0.5)

        # Score brut combinant utilisateurs uniques et clics totaux
        popularity['raw_score'] = (
            0.7 * popularity['unique_users'] + 0.3 * popularity['total_clicks']
        )

        # Score normalisé par l'âge de l'article (clics par mois d'existence)
        popularity['popularity_score'] = popularity['raw_score'] / popularity['article_age_months']

        result = popularity.sort_values('popularity_score', ascending=False)
        logger.info(f"📈 Articles populaires calculés: {len(result):,} articles (normalisés par âge)")

        return result
    
    def get_all_users(self) -> List[int]:
        """Récupère la liste de tous les utilisateurs"""
        interactions = self.load_user_interactions()
        return sorted(interactions['user_id'].unique().tolist())
    
    def get_article_info(self, article_id: int) -> Dict:
        """Récupère les informations d'un article"""
        metadata = self.load_articles_metadata()
        article = metadata[metadata['article_id'] == article_id]
        
        if len(article) == 0:
            return {"error": "Article not found"}
        
        article_dict = article.iloc[0].to_dict()
        
        # Conversion des types numpy pour la sérialisation JSON
        for key, value in article_dict.items():
            if hasattr(value, 'item'):  # numpy types
                article_dict[key] = value.item()
            elif pd.isna(value):
                article_dict[key] = None
                
        return article_dict
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Statistiques d'un utilisateur"""
        history = self.get_user_history(user_id)

        if len(history) == 0:
            return {
                "user_id": user_id,
                "total_interactions": 0,
                "unique_articles": 0,
                "date_range": {
                    "first_interaction": None,
                    "last_interaction": None
                },
                "top_categories": [],
                "is_new_user": True
            }
        
        # Catégories les plus consultées
        categories = []
        if len(history) > 0:
            metadata = self.load_articles_metadata()
            merged = history.merge(metadata[['article_id', 'category_id']], 
                                 left_on='click_article_id', 
                                 right_on='article_id', 
                                 how='left')
            if len(merged) > 0:
                cat_counts = merged['category_id'].value_counts().head(5)
                categories = [{"category_id": int(cat), "count": int(count)} 
                            for cat, count in cat_counts.items()]
        
        return {
            "user_id": user_id,
            "total_interactions": len(history),
            "unique_articles": history['click_article_id'].nunique(),
            "date_range": {
                "first_interaction": history['click_datetime'].min().isoformat() if len(history) > 0 else None,
                "last_interaction": history['click_datetime'].max().isoformat() if len(history) > 0 else None
            },
            "top_categories": categories
        }
    
    def get_data_stats(self) -> Dict:
        """Statistiques générales des données"""
        try:
            metadata = self.load_articles_metadata()
            interactions = self.load_user_interactions()
            recommendable = self.get_recommendable_articles()
            reference_date = self._get_reference_date()
            
            return {
                "total_articles": len(metadata),
                "recommendable_articles": len(recommendable),
                "total_interactions": len(interactions),
                "unique_users": interactions['user_id'].nunique() if len(interactions) > 0 else 0,
                "reference_date": reference_date.isoformat(),
                "data_loaded": True
            }
        except Exception as e:
            logger.error(f"❌ Erreur lors du calcul des stats: {e}")
            return {
                "error": str(e),
                "data_loaded": False
            }

# Instance globale
data_loader = DataLoader()