# backend/main.py
import logging
from datetime import datetime
from typing import List, Optional
import uvicorn

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from models import (
    RecommendationRequest, 
    RecommendationResponse, 
    UserSegmentInfo,
    HealthResponse
)
from data_loader import data_loader
from recommenders import (
    PopularityRecommender,
    ContentRecommender,
    ClusteringRecommender,
    HybridRecommender
)
from config import settings

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="API de recommandation My Content",
    description="API de recommandation d'articles pour My Content",
    version="1.0.0"
)

# Middleware CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instances des recommandeurs (lazy loading)
recommenders = {}

def get_recommender(method: str):
    """Factory pour créer les recommandeurs"""
    if method not in recommenders:
        if method == "popularity":
            recommenders[method] = PopularityRecommender(data_loader)
        elif method == "content":
            recommenders[method] = ContentRecommender(data_loader)
        elif method == "clustering":
            recommenders[method] = ClusteringRecommender(data_loader)
        elif method == "hybrid":
            recommenders[method] = HybridRecommender(data_loader)
        else:
            raise ValueError(f"Méthode de recommandation inconnue: {method}")
        
        logger.info(f"📦 Recommandeur {method} initialisé")
    
    return recommenders[method]

# =======================
# ENDPOINTS PRINCIPAUX
# =======================

@app.get("/", response_model=dict)
async def root():
    """Endpoint racine"""
    return {
        "message": "My Content Recommender API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Vérification de l'état de santé de l'API"""
    try:
        data_stats = data_loader.get_data_stats()
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version="1.0.0",
            data_stats=data_stats
        )
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/recommend/{user_id}", response_model=RecommendationResponse)
async def recommend_for_user(
    user_id: int,
    method: str = "hybrid",
    n_recommendations: int = 5,
    exclude_seen: bool = True
):
    """
    Génère des recommandations pour un utilisateur
    
    - **user_id**: ID de l'utilisateur
    - **method**: Méthode de recommandation (popularity, content, clustering, hybrid)
    - **n_recommendations**: Nombre de recommandations (max 20)
    - **exclude_seen**: Exclure les articles déjà vus
    """
    # Validation des paramètres
    if method not in ["popularity", "content", "clustering", "hybrid"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Méthode '{method}' non supportée. Utilisez: popularity, content, clustering, hybrid"
        )
    
    if n_recommendations > 20:
        raise HTTPException(status_code=400, detail="Maximum 20 recommandations")
    
    if n_recommendations < 1:
        raise HTTPException(status_code=400, detail="Minimum 1 recommandation")
    
    try:
        # Vérifier que l'utilisateur existe
        all_users = data_loader.get_all_users()
        if user_id not in all_users:
            raise HTTPException(
                status_code=404, 
                detail=f"Utilisateur {user_id} non trouvé"
            )
        
        # Générer les recommandations
        logger.info(f"🎯 Génération recommandations: user={user_id}, method={method}, n={n_recommendations}")
        
        recommender = get_recommender(method)
        recommendations = recommender.recommend(
            user_id=user_id,
            n_recommendations=n_recommendations,
            exclude_seen=exclude_seen
        )
        
        # Métadonnées sur la recommandation
        user_stats = data_loader.get_user_stats(user_id)
        metadata = {
            "method": method,
            "parameters": {
                "n_recommendations": n_recommendations,
                "exclude_seen": exclude_seen
            },
            "user_stats": user_stats,
            "results_count": len(recommendations)
        }
        
        return RecommendationResponse(
            user_id=user_id,
            method=method,
            recommendations=recommendations,
            metadata=metadata,
            generated_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur recommandation user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/users", response_model=List[int])
async def get_users(limit: int = 100):
    """
    Liste des utilisateurs disponibles (pour tests)
    
    - **limit**: Nombre maximum d'utilisateurs à retourner
    """
    try:
        all_users = data_loader.get_all_users()
        
        if limit > 1000:
            limit = 1000
            
        return all_users[:limit]
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération utilisateurs: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/users/{user_id}/stats", response_model=dict)
async def get_user_stats(user_id: int):
    """
    Statistiques d'un utilisateur
    
    - **user_id**: ID de l'utilisateur
    """
    try:
        stats = data_loader.get_user_stats(user_id)
        
        if "error" in stats:
            raise HTTPException(status_code=404, detail=stats["error"])
            
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur stats user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/users/{user_id}/segment", response_model=UserSegmentInfo)
async def get_user_segment(user_id: int):
    """
    Informations sur le segment/cluster d'un utilisateur
    
    - **user_id**: ID de l'utilisateur
    """
    try:
        # Vérifier que l'utilisateur existe
        all_users = data_loader.get_all_users()
        if user_id not in all_users:
            raise HTTPException(
                status_code=404, 
                detail=f"Utilisateur {user_id} non trouvé"
            )
        
        clustering_rec = get_recommender("clustering")
        segment_info = clustering_rec.get_user_segment_info(user_id)
        
        return UserSegmentInfo(**segment_info)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur segment user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/articles/{article_id}", response_model=dict)
async def get_article_info(article_id: int):
    """
    Informations sur un article
    
    - **article_id**: ID de l'article
    """
    try:
        article_info = data_loader.get_article_info(article_id)
        
        if "error" in article_info:
            raise HTTPException(status_code=404, detail=article_info["error"])
            
        return article_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur article {article_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/popular", response_model=List[dict])
async def get_popular_articles(limit: int = 10):
    """
    Articles populaires récemment

    - **limit**: Nombre d'articles à retourner (max 50)
    """
    try:
        if limit > 50:
            limit = 50

        popular = data_loader.get_recent_popular_articles()

        results = []
        for i, (article_id, row) in enumerate(popular.head(limit).iterrows()):
            article_info = data_loader.get_article_info(article_id)
            results.append({
                "rank": i + 1,
                "article_id": article_id,
                "popularity_score": float(row['popularity_score']),
                "unique_users": int(row['unique_users']),
                "total_clicks": int(row['total_clicks']),
                "metadata": article_info
            })

        return results

    except Exception as e:
        logger.error(f"❌ Erreur articles populaires: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

@app.get("/clusters", response_model=dict)
async def get_clusters_characteristics():
    """
    Caractéristiques de tous les segments/clusters d'utilisateurs

    Retourne les informations détaillées sur chaque cluster :
    - Taille (nombre d'utilisateurs)
    - Activité moyenne (clics, diversité des catégories)
    - Préférences (longueur des articles)
    - Niveau d'engagement
    """
    try:
        clustering_rec = get_recommender("clustering")

        # Déclencher le calcul des clusters si nécessaire
        if clustering_rec._cluster_characteristics is None:
            clustering_rec._get_user_cluster(1)  # Force le calcul avec un user dummy

        if clustering_rec._cluster_characteristics is None:
            raise HTTPException(
                status_code=503,
                detail="Clusters non disponibles - pas assez de données"
            )

        clusters_info = {
            "total_clusters": len(clustering_rec._cluster_characteristics),
            "last_training": clustering_rec._last_training.isoformat() if clustering_rec._last_training else None,
            "clusters": {}
        }

        total_users = sum(char['size'] for char in clustering_rec._cluster_characteristics.values())

        for cluster_id, characteristics in clustering_rec._cluster_characteristics.items():
            clusters_info["clusters"][str(cluster_id)] = {
                "cluster_id": cluster_id,
                "size": characteristics['size'],
                "percentage": round((characteristics['size'] / total_users) * 100, 1) if total_users > 0 else 0,
                "characteristics": {
                    "avg_clicks": round(characteristics['avg_clicks'], 1),
                    "avg_diversity": round(characteristics['avg_diversity'], 1),
                    "avg_words_preference": round(characteristics['avg_words_preference'], 0),
                    "activity_level": round(characteristics['activity_level'], 3)
                },
                "description": _generate_cluster_description(characteristics)
            }

        clusters_info["summary"] = {
            "total_users_clustered": total_users,
            "most_active_cluster": max(clustering_rec._cluster_characteristics.items(),
                                     key=lambda x: x[1]['activity_level'])[0],
            "largest_cluster": max(clustering_rec._cluster_characteristics.items(),
                                 key=lambda x: x[1]['size'])[0]
        }

        return clusters_info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur récupération clusters: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

def _generate_cluster_description(characteristics: dict) -> str:
    """Génère une description textuelle d'un cluster"""
    size = characteristics['size']
    avg_clicks = characteristics['avg_clicks']
    diversity = characteristics['avg_diversity']
    activity = characteristics['activity_level']

    # Classifier le niveau d'activité basé sur le nombre total de clics
    if avg_clicks > 20:
        activity_level = "très actifs"
    elif avg_clicks > 5:
        activity_level = "modérément actifs"
    else:
        activity_level = "peu actifs"

    # Classifier la diversité
    if diversity > 5:
        diversity_level = "éclectiques"
    elif diversity > 3:
        diversity_level = "diversifiés"
    else:
        diversity_level = "spécialisés"

    return f"Cluster de {size} utilisateurs {activity_level} ({avg_clicks:.0f} clics moy.), {diversity_level} ({diversity:.1f} catégories moy.), niveau d'activité: {activity:.2f}"

# =======================
# ENDPOINTS DEBUG
# =======================

@app.get("/debug/config", response_model=dict)
async def get_config():
    """Configuration actuelle (debug)"""
    return {
        "DATA_PATH": str(settings.DATA_PATH),
        "POPULARITY_WINDOW_DAYS": settings.POPULARITY_WINDOW_DAYS,
        "MAX_ARTICLE_AGE_DAYS": settings.MAX_ARTICLE_AGE_DAYS,
        "MIN_WORDS_COUNT": settings.MIN_WORDS_COUNT,
        "N_RECOMMENDATIONS": settings.N_RECOMMENDATIONS,
        "N_USER_CLUSTERS": settings.N_USER_CLUSTERS,
        "HYBRID_WEIGHTS": settings.HYBRID_WEIGHTS,
        "MIN_USER_INTERACTIONS": settings.MIN_USER_INTERACTIONS
    }

@app.get("/debug/data-stats", response_model=dict)
async def get_detailed_data_stats():
    """Statistiques détaillées des données (debug)"""
    try:
        stats = data_loader.get_data_stats()
        
        # Statistiques additionnelles
        interactions = data_loader.load_user_interactions()
        metadata = data_loader.load_articles_metadata()
        
        additional_stats = {
            "categories_count": metadata['category_id'].nunique(),
            "avg_words_per_article": metadata['words_count'].mean(),
            "interactions_per_user": interactions.groupby('user_id')['click_article_id'].count().mean() if len(interactions) > 0 else 0,
            "date_range": {
                "min_article_date": metadata['created_date'].min().isoformat(),
                "max_article_date": metadata['created_date'].max().isoformat(),
            } if len(metadata) > 0 else {}
        }
        
        stats.update(additional_stats)
        return stats
        
    except Exception as e:
        logger.error(f"❌ Erreur stats détaillées: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur interne: {str(e)}")

# =======================
# GESTION DES ERREURS
# =======================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Ressource non trouvée", "detail": str(exc.detail)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Erreur interne du serveur", "detail": str(exc.detail)}

# =======================
# POINT D'ENTRÉE
# =======================

if __name__ == "__main__":
    logger.info("🚀 Démarrage de My Content Recommender API")
    
    # Préchargement des données (optionnel)
    try:
        logger.info("📊 Préchargement des données...")
        data_stats = data_loader.get_data_stats()
        logger.info(f"✅ Données chargées: {data_stats}")
    except Exception as e:
        logger.error(f"⚠️ Erreur préchargement: {e}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )