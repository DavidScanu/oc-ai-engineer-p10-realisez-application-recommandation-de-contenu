# backend/scripts/analyze_articles_metadata.py
import pandas as pd
from pathlib import Path

def analyze_articles_metadata():
    """Analyse complète du fichier articles_metadata.csv"""
    
    data_path = Path("backend/data/articles_metadata.csv")
    
    if not data_path.exists():
        print("❌ Fichier articles_metadata.csv non trouvé")
        return
    
    print("📊 ANALYSE DU FICHIER ARTICLES_METADATA.CSV")
    print("=" * 60)
    
    # Charger les données
    df = pd.read_csv(data_path)
    print(f"🔍 Dataset chargé: {len(df):,} articles")
    
    # ========== INFORMATIONS GÉNÉRALES ==========
    print("\n" + "=" * 40)
    print("📋 INFORMATIONS GÉNÉRALES")
    print("=" * 40)
    
    print(f"📄 Nombre total d'articles: {len(df):,}")
    print(f"📊 Nombre de colonnes: {len(df.columns)}")
    print(f"📝 Colonnes: {list(df.columns)}")
    print(f"💾 Taille en mémoire: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
    
    # Valeurs manquantes
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"\n⚠️  Valeurs manquantes:")
        for col, count in missing.items():
            if count > 0:
                print(f"   - {col}: {count:,} ({count/len(df)*100:.1f}%)")
    else:
        print("\n✅ Aucune valeur manquante")
    
    # ========== ANALYSE DES ARTICLES ==========
    print("\n" + "=" * 40)
    print("📄 ANALYSE DES ARTICLES")
    print("=" * 40)
    
    print(f"🆔 Article ID min: {df['article_id'].min():,}")
    print(f"🆔 Article ID max: {df['article_id'].max():,}")
    print(f"🔢 Nombre d'IDs uniques: {df['article_id'].nunique():,}")
    
    if df['article_id'].nunique() != len(df):
        duplicates = len(df) - df['article_id'].nunique()
        print(f"⚠️  Doublons détectés: {duplicates:,}")
    else:
        print("✅ Tous les article_id sont uniques")
    
    # ========== ANALYSE DES CATÉGORIES ==========
    print("\n" + "=" * 40)
    print("🏷️  ANALYSE DES CATÉGORIES")
    print("=" * 40)
    
    category_counts = df['category_id'].value_counts().head(10)
    print(f"📊 Nombre de catégories uniques: {df['category_id'].nunique():,}")
    print(f"📈 Distribution des top 10 catégories:")
    for cat_id, count in category_counts.items():
        percentage = count / len(df) * 100
        print(f"   - Catégorie {cat_id}: {count:,} articles ({percentage:.1f}%)")
    
    # Statistiques des catégories
    print(f"\n📊 Statistiques des catégories:")
    print(f"   - Moyenne d'articles par catégorie: {len(df) / df['category_id'].nunique():.1f}")
    print(f"   - Médiane d'articles par catégorie: {df['category_id'].value_counts().median():.1f}")
    print(f"   - Catégorie la plus représentée: {df['category_id'].mode().iloc[0]} ({category_counts.iloc[0]:,} articles)")
    
    # ========== ANALYSE DES ÉDITEURS ==========
    print("\n" + "=" * 40)
    print("📰 ANALYSE DES ÉDITEURS")
    print("=" * 40)
    
    publisher_counts = df['publisher_id'].value_counts().head(10)
    print(f"🏢 Nombre d'éditeurs uniques: {df['publisher_id'].nunique():,}")
    print(f"📈 Distribution des top 10 éditeurs:")
    for pub_id, count in publisher_counts.items():
        percentage = count / len(df) * 100
        print(f"   - Éditeur {pub_id}: {count:,} articles ({percentage:.1f}%)")
    
    # ========== ANALYSE DES DATES ==========
    print("\n" + "=" * 40)
    print("📅 ANALYSE DES DATES DE CRÉATION")
    print("=" * 40)
    
    # Convertir les timestamps en dates
    df['created_date'] = pd.to_datetime(df['created_at_ts'], unit='ms')
    
    print(f"📅 Date la plus ancienne: {df['created_date'].min().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Date la plus récente: {df['created_date'].max().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Période couverte: {(df['created_date'].max() - df['created_date'].min()).days:,} jours")
    
    # Articles par année
    df['year'] = df['created_date'].dt.year
    yearly_counts = df['year'].value_counts().sort_index()
    print(f"\n📈 Articles par année:")
    for year, count in yearly_counts.items():
        print(f"   - {year}: {count:,} articles")
    
    # Articles par mois (dernière année)
    latest_year = df['year'].max()
    latest_year_data = df[df['year'] == latest_year]
    if len(latest_year_data) > 0:
        monthly_counts = latest_year_data['created_date'].dt.month.value_counts().sort_index()
        print(f"\n📈 Articles par mois en {latest_year}:")
        months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                  'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
        for month, count in monthly_counts.items():
            print(f"   - {months[month-1]}: {count:,} articles")
    
    # ========== ANALYSE DU NOMBRE DE MOTS ==========
    print("\n" + "=" * 40)
    print("📝 ANALYSE DU NOMBRE DE MOTS")
    print("=" * 40)
    
    words_stats = df['words_count'].describe()
    print(f"📊 Statistiques du nombre de mots:")
    print(f"   - Minimum: {words_stats['min']:.0f} mots")
    print(f"   - Maximum: {words_stats['max']:.0f} mots")
    print(f"   - Moyenne: {words_stats['mean']:.0f} mots")
    print(f"   - Médiane: {words_stats['50%']:.0f} mots")
    print(f"   - Écart-type: {words_stats['std']:.0f} mots")
    
    # Distribution par tranches
    print(f"\n📈 Distribution par tranches de mots:")
    bins = [0, 100, 200, 300, 500, 1000, float('inf')]
    labels = ['0-100', '101-200', '201-300', '301-500', '501-1000', '1000+']
    df['word_range'] = pd.cut(df['words_count'], bins=bins, labels=labels, right=True)
    word_distribution = df['word_range'].value_counts().sort_index()
    
    for range_label, count in word_distribution.items():
        percentage = count / len(df) * 100
        print(f"   - {range_label} mots: {count:,} articles ({percentage:.1f}%)")
    
    # ========== CORRÉLATIONS ET INSIGHTS ==========
    print("\n" + "=" * 40)
    print("🔍 INSIGHTS ET CORRÉLATIONS")
    print("=" * 40)
    
    # Nombre moyen de mots par catégorie
    avg_words_by_category = df.groupby('category_id')['words_count'].mean().sort_values(ascending=False).head(5)
    print(f"📊 Top 5 des catégories avec le plus de mots en moyenne:")
    for cat_id, avg_words in avg_words_by_category.items():
        print(f"   - Catégorie {cat_id}: {avg_words:.0f} mots en moyenne")
    
    # Nombre moyen de mots par éditeur
    avg_words_by_publisher = df.groupby('publisher_id')['words_count'].mean().sort_values(ascending=False).head(5)
    print(f"\n📊 Top 5 des éditeurs avec le plus de mots en moyenne:")
    for pub_id, avg_words in avg_words_by_publisher.items():
        print(f"   - Éditeur {pub_id}: {avg_words:.0f} mots en moyenne")
    
    # Évolution du nombre de mots dans le temps
    monthly_avg_words = df.groupby(df['created_date'].dt.to_period('M'))['words_count'].mean()
    if len(monthly_avg_words) > 1:
        trend = "croissant" if monthly_avg_words.iloc[-1] > monthly_avg_words.iloc[0] else "décroissant"
        print(f"\n📈 Tendance du nombre de mots: {trend}")
        print(f"   - Premier mois: {monthly_avg_words.iloc[0]:.0f} mots en moyenne")
        print(f"   - Dernier mois: {monthly_avg_words.iloc[-1]:.0f} mots en moyenne")
    
    # ========== RÉSUMÉ ==========
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ EXÉCUTIF")
    print("=" * 60)
    
    print(f"✅ Dataset de {len(df):,} articles sur {(df['created_date'].max() - df['created_date'].min()).days:,} jours")
    print(f"✅ {df['category_id'].nunique():,} catégories différentes")
    print(f"✅ {df['publisher_id'].nunique():,} éditeurs différents")
    print(f"✅ Articles de {words_stats['min']:.0f} à {words_stats['max']:.0f} mots ({words_stats['mean']:.0f} en moyenne)")
    print(f"✅ Période: {df['created_date'].min().strftime('%Y-%m-%d')} à {df['created_date'].max().strftime('%Y-%m-%d')}")
    
    # Détection d'anomalies potentielles
    print(f"\n🔍 POINTS D'ATTENTION:")
    
    # Articles très courts ou très longs
    very_short = len(df[df['words_count'] < 50])
    very_long = len(df[df['words_count'] > 2000])
    
    if very_short > 0:
        print(f"⚠️  {very_short:,} articles très courts (< 50 mots) - {very_short/len(df)*100:.1f}%")
    
    if very_long > 0:
        print(f"⚠️  {very_long:,} articles très longs (> 2000 mots) - {very_long/len(df)*100:.1f}%")
    
    # Concentration des catégories
    top_category_pct = category_counts.iloc[0] / len(df) * 100
    if top_category_pct > 30:
        print(f"⚠️  La catégorie dominante représente {top_category_pct:.1f}% des articles")
    
    # Concentration des éditeurs
    top_publisher_pct = publisher_counts.iloc[0] / len(df) * 100
    if top_publisher_pct > 50:
        print(f"⚠️  L'éditeur dominant représente {top_publisher_pct:.1f}% des articles")
    
    return {
        'total_articles': len(df),
        'categories': df['category_id'].nunique(),
        'publishers': df['publisher_id'].nunique(),
        'date_range': (df['created_date'].min(), df['created_date'].max()),
        'words_stats': words_stats.to_dict(),
        'top_categories': category_counts.head(5).to_dict(),
        'top_publishers': publisher_counts.head(5).to_dict()
    }

if __name__ == "__main__":
    stats = analyze_articles_metadata()