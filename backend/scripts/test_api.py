# backend/scripts/test_api.py
import requests
import json
from typing import Dict, Any

class APITester:
    """Testeur pour l'API de recommandation"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def test_health(self) -> Dict[str, Any]:
        """Test du endpoint health"""
        print("🏥 Test Health Check...")
        response = requests.get(f"{self.base_url}/health")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API Status: {result['status']}")
            print(f"📊 Data Stats: {result['data_stats']}")
            return result
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return {}
    
    def test_users_list(self, limit: int = 10) -> list:
        """Test récupération des utilisateurs"""
        print(f"\n👥 Test Users List (limit={limit})...")
        response = requests.get(f"{self.base_url}/users?limit={limit}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"✅ {len(users)} utilisateurs récupérés")
            print(f"📝 Premiers utilisateurs: {users[:5]}")
            return users
        else:
            print(f"❌ Users list failed: {response.status_code}")
            return []
    
    def test_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Test stats d'un utilisateur"""
        print(f"\n📊 Test User Stats (user_id={user_id})...")
        response = requests.get(f"{self.base_url}/users/{user_id}/stats")
        
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats récupérées:")
            print(f"   - Interactions: {stats['total_interactions']}")
            print(f"   - Articles uniques: {stats['unique_articles']}")
            print(f"   - Top catégories: {len(stats['top_categories'])}")
            return stats
        else:
            print(f"❌ User stats failed: {response.status_code}")
            return {}
    
    def test_recommendations(self, user_id: int, method: str = "hybrid") -> Dict[str, Any]:
        """Test recommandations"""
        print(f"\n🎯 Test Recommendations (user_id={user_id}, method={method})...")
        response = requests.post(
            f"{self.base_url}/recommend/{user_id}?method={method}&n_recommendations=5"
        )
        
        if response.status_code == 200:
            result = response.json()
            recommendations = result['recommendations']
            print(f"✅ {len(recommendations)} recommandations générées:")
            
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. Article {rec['article_id']} (score: {rec['score']:.3f})")
                print(f"      Raison: {rec['reason'][:80]}...")
                
            return result
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
            print(f"    Error: {response.text}")
            return {}
    
    def test_all_methods(self, user_id: int):
        """Test toutes les méthodes de recommandation"""
        methods = ["popularity", "content", "clustering", "hybrid"]
        
        print(f"\n🎭 Test toutes les méthodes pour user {user_id}")
        print("=" * 60)
        
        results = {}
        for method in methods:
            try:
                result = self.test_recommendations(user_id, method)
                results[method] = len(result.get('recommendations', []))
            except Exception as e:
                print(f"❌ Erreur {method}: {e}")
                results[method] = 0
        
        print(f"\n📊 Résumé des recommandations:")
        for method, count in results.items():
            print(f"   - {method}: {count} recommandations")
    
    def test_popular_articles(self, limit: int = 10):
        """Test articles populaires"""
        print(f"\n🔥 Test Popular Articles (limit={limit})...")
        response = requests.get(f"{self.base_url}/popular?limit={limit}")
        
        if response.status_code == 200:
            articles = response.json()
            print(f"✅ {len(articles)} articles populaires:")
            
            for article in articles[:5]:
                print(f"   {article['rank']}. Article {article['article_id']} "
                      f"(score: {article['popularity_score']:.1f}, "
                      f"{article['unique_users']} users)")
                
        else:
            print(f"❌ Popular articles failed: {response.status_code}")
    
    def run_full_test(self):
        """Lance tous les tests"""
        print("🚀 LANCEMENT DES TESTS COMPLETS")
        print("=" * 60)
        
        # 1. Health check
        health = self.test_health()
        if not health:
            print("❌ API non disponible, arrêt des tests")
            return
        
        # 2. Récupérer quelques utilisateurs
        users = self.test_users_list(20)
        if not users:
            print("❌ Aucun utilisateur trouvé, arrêt des tests")
            return
        
        # 3. Tester avec un utilisateur
        test_user = users[0]
        
        # Stats utilisateur
        self.test_user_stats(test_user)
        
        # Toutes les méthodes de recommandation
        self.test_all_methods(test_user)
        
        # Articles populaires
        self.test_popular_articles()
        
        print(f"\n✅ TESTS TERMINÉS")

if __name__ == "__main__":
    tester = APITester()
    tester.run_full_test()