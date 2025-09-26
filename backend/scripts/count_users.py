# backend/scripts/count_users.py
import pandas as pd
import glob
import os
from pathlib import Path

def count_users_and_articles():
    """Compte le nombre d'utilisateurs uniques et d'articles dans les données"""
    
    data_path = Path("backend/data")
    clicks_path = data_path / "clicks"
    
    print("🔍 Analyse des données...")
    
    # Compter dans tous les fichiers clicks
    all_users = set()
    all_articles = set()
    total_clicks = 0
    
    # Lire tous les fichiers clicks_hour_*.csv
    click_files = glob.glob(str(clicks_path / "clicks_hour_*.csv"))
    print(f"📁 Nombre de fichiers trouvés: {len(click_files)}")
    
    for file_path in click_files:
        try:
            df = pd.read_csv(file_path)
            all_users.update(df['user_id'].unique())
            all_articles.update(df['click_article_id'].unique())
            total_clicks += len(df)
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    # Compter dans articles_metadata.csv
    metadata_path = data_path / "articles_metadata.csv"
    if metadata_path.exists():
        metadata_df = pd.read_csv(metadata_path)
        total_articles_metadata = len(metadata_df)
        print(f"📊 Articles dans metadata: {total_articles_metadata}")
    
    print("\n" + "="*50)
    print("📈 RÉSULTATS")
    print("="*50)
    print(f"👥 Utilisateurs uniques: {len(all_users):,}")
    print(f"📄 Articles uniques (dans clicks): {len(all_articles):,}")
    print(f"🖱️  Total des clics: {total_clicks:,}")
    print(f"📊 Moyenne clics/utilisateur: {total_clicks/len(all_users):.1f}")
    print(f"📊 Moyenne clics/article: {total_clicks/len(all_articles):.1f}")
    
    return {
        'users': len(all_users),
        'articles': len(all_articles),
        'clicks': total_clicks,
        'avg_clicks_per_user': total_clicks/len(all_users),
        'avg_clicks_per_article': total_clicks/len(all_articles)
    }

if __name__ == "__main__":
    stats = count_users_and_articles()