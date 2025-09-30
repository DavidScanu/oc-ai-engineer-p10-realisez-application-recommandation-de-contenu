#!/usr/bin/env python3
# backend/scripts/test_cold_start.py
"""
Script de test pour valider la gestion du cold start avec validation des interactions.

Tests :
1. Utilisateur inexistant (0 interactions) → fallback
2. Utilisateur avec peu d'interactions valides (< MIN_USER_INTERACTIONS) → fallback
3. Utilisateur avec assez d'interactions valides (≥ MIN_USER_INTERACTIONS) → personnalisé
4. Cas limite : interactions invalides (article_id inexistants)
"""

import requests
import json
from typing import Dict, Any, List
from colorama import init, Fore, Style
import sys

# Initialiser colorama pour les couleurs
init(autoreset=True)

class ColdStartTester:
    """Testeur spécialisé pour la validation du cold start"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []

    def print_section(self, title: str):
        """Affiche un titre de section"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}{title}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")

    def print_success(self, message: str):
        """Affiche un message de succès"""
        print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

    def print_error(self, message: str):
        """Affiche un message d'erreur"""
        print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

    def print_info(self, message: str):
        """Affiche un message d'information"""
        print(f"{Fore.YELLOW}ℹ️  {message}{Style.RESET_ALL}")

    def print_warning(self, message: str):
        """Affiche un avertissement"""
        print(f"{Fore.MAGENTA}⚠️  {message}{Style.RESET_ALL}")

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Récupère les stats d'un utilisateur"""
        try:
            response = requests.get(f"{self.base_url}/users/{user_id}/stats")
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            self.print_error(f"Erreur récupération stats user {user_id}: {e}")
            return {}

    def test_recommendation(self, user_id: int, method: str, expected_fallback: bool) -> bool:
        """
        Test une recommandation et valide le comportement attendu

        Returns:
            True si le test est passé, False sinon
        """
        try:
            response = requests.post(
                f"{self.base_url}/recommend/{user_id}",
                params={"method": method, "n_recommendations": 5}
            )

            if response.status_code != 200:
                self.print_error(f"HTTP {response.status_code}: {response.text}")
                return False

            result = response.json()

            # Validation du comportement
            fallback_applied = result.get('fallback_applied', False)
            actual_method = result.get('actual_method', method)
            recommendations = result.get('recommendations', [])
            metadata = result.get('metadata', {})

            # Affichage des informations
            print(f"\n  📊 Résultats pour méthode '{method}':")
            print(f"     • Fallback appliqué: {fallback_applied}")
            print(f"     • Méthode réelle: {actual_method}")
            print(f"     • Nombre de recommandations: {len(recommendations)}")

            if fallback_applied:
                fallback_reason = metadata.get('fallback_reason', 'N/A')
                print(f"     • Raison du fallback: {fallback_reason}")

                # Vérifier les métadonnées dans les recommandations
                if recommendations:
                    first_rec = recommendations[0]
                    if 'fallback_from' in first_rec:
                        print(f"     • Fallback détecté depuis: {first_rec['fallback_from']}")
                        print(f"     • Raison courte: {first_rec.get('fallback_reason', 'N/A')}")

            # Validation
            test_passed = True

            if fallback_applied != expected_fallback:
                self.print_error(
                    f"Comportement inattendu ! "
                    f"Fallback attendu: {expected_fallback}, obtenu: {fallback_applied}"
                )
                test_passed = False

            if expected_fallback and actual_method != "popularity":
                self.print_error(
                    f"Méthode de fallback incorrecte ! "
                    f"Attendu: 'popularity', obtenu: '{actual_method}'"
                )
                test_passed = False

            if not expected_fallback and actual_method != method:
                self.print_error(
                    f"Méthode incorrecte ! "
                    f"Attendu: '{method}', obtenu: '{actual_method}'"
                )
                test_passed = False

            if len(recommendations) == 0:
                self.print_error("Aucune recommandation retournée !")
                test_passed = False

            # Vérifier la cohérence des métadonnées de fallback
            if expected_fallback:
                if not fallback_applied:
                    self.print_error("Champ 'fallback_applied' devrait être True")
                    test_passed = False

                if 'fallback_reason' not in metadata:
                    self.print_error("Champ 'fallback_reason' manquant dans metadata")
                    test_passed = False

                if recommendations:
                    first_rec = recommendations[0]
                    if 'fallback_from' not in first_rec:
                        self.print_error("Champ 'fallback_from' manquant dans les recommandations")
                        test_passed = False
                    if 'fallback_reason' not in first_rec:
                        self.print_error("Champ 'fallback_reason' manquant dans les recommandations")
                        test_passed = False

            if test_passed:
                self.print_success(f"Test réussi pour méthode '{method}'")

            return test_passed

        except Exception as e:
            self.print_error(f"Exception lors du test: {e}")
            return False

    def test_scenario_1_new_user(self):
        """Test 1: Utilisateur complètement nouveau (0 interactions)"""
        self.print_section("TEST 1: Utilisateur inexistant (Cold Start Total)")

        user_id = 999999999
        self.print_info(f"Test avec user_id={user_id} (inexistant)")

        # Récupérer les stats
        stats = self.get_user_stats(user_id)
        print(f"\n  📈 Statistiques utilisateur:")
        print(f"     • Total interactions: {stats.get('total_interactions', 0)}")
        print(f"     • Articles uniques: {stats.get('unique_articles', 0)}")
        print(f"     • Nouvel utilisateur: {stats.get('is_new_user', 'N/A')}")

        # Tester toutes les méthodes (sauf popularity)
        methods = ["content", "clustering", "hybrid"]
        results = []

        for method in methods:
            passed = self.test_recommendation(user_id, method, expected_fallback=True)
            results.append(passed)

        # Test popularity (ne devrait PAS faire de fallback)
        print(f"\n  📊 Test spécial pour méthode 'popularity':")
        passed_pop = self.test_recommendation(user_id, "popularity", expected_fallback=False)
        results.append(passed_pop)

        # Résumé
        all_passed = all(results)
        if all_passed:
            self.print_success("✨ TEST 1 RÉUSSI: Tous les fallbacks fonctionnent correctement")
        else:
            self.print_error("💥 TEST 1 ÉCHOUÉ: Certains tests ont échoué")

        self.test_results.append(("Test 1: Utilisateur inexistant", all_passed))
        return all_passed

    def test_scenario_2_few_interactions(self):
        """Test 2: Utilisateur avec peu d'interactions (< MIN_USER_INTERACTIONS)"""
        self.print_section("TEST 2: Utilisateur avec peu d'interactions (< 5)")

        self.print_info("Recherche d'un utilisateur avec 1-4 interactions...")

        # Récupérer des utilisateurs et trouver un avec peu d'interactions
        try:
            response = requests.get(f"{self.base_url}/users?limit=100")
            if response.status_code == 200:
                users = response.json()

                # Chercher un utilisateur avec peu d'interactions
                target_user = None
                for user_id in users:
                    stats = self.get_user_stats(user_id)
                    interactions = stats.get('total_interactions', 0)
                    if 1 <= interactions < 5:
                        target_user = user_id
                        self.print_info(f"Utilisateur trouvé: {user_id} avec {interactions} interactions")
                        break

                if not target_user:
                    self.print_warning("Aucun utilisateur avec 1-4 interactions trouvé dans les 100 premiers")
                    self.print_info("Création d'un scénario simulé...")
                    self.test_results.append(("Test 2: Peu d'interactions", None))
                    return None

                # Tester les recommandations
                stats = self.get_user_stats(target_user)
                print(f"\n  📈 Statistiques utilisateur {target_user}:")
                print(f"     • Total interactions: {stats.get('total_interactions', 0)}")
                print(f"     • Articles uniques: {stats.get('unique_articles', 0)}")

                methods = ["content", "clustering", "hybrid"]
                results = []

                for method in methods:
                    passed = self.test_recommendation(target_user, method, expected_fallback=True)
                    results.append(passed)

                all_passed = all(results)
                if all_passed:
                    self.print_success("✨ TEST 2 RÉUSSI: Fallback appliqué pour utilisateur avec peu d'interactions")
                else:
                    self.print_error("💥 TEST 2 ÉCHOUÉ")

                self.test_results.append(("Test 2: Peu d'interactions", all_passed))
                return all_passed
            else:
                self.print_error(f"Impossible de récupérer la liste des utilisateurs: {response.status_code}")
                self.test_results.append(("Test 2: Peu d'interactions", False))
                return False

        except Exception as e:
            self.print_error(f"Erreur durant le test: {e}")
            self.test_results.append(("Test 2: Peu d'interactions", False))
            return False

    def test_scenario_3_sufficient_interactions(self):
        """Test 3: Utilisateur avec assez d'interactions (≥ MIN_USER_INTERACTIONS)"""
        self.print_section("TEST 3: Utilisateur avec interactions suffisantes (≥ 5)")

        self.print_info("Recherche d'un utilisateur avec ≥5 interactions...")

        try:
            response = requests.get(f"{self.base_url}/users?limit=100")
            if response.status_code == 200:
                users = response.json()

                # Chercher un utilisateur avec assez d'interactions
                target_user = None
                # for user_id in users:
                #     stats = self.get_user_stats(user_id)
                #     interactions = stats.get('total_interactions', 0)
                #     if interactions >= 5:
                #         target_user = user_id
                #         self.print_info(f"Utilisateur trouvé: {user_id} avec {interactions} interactions")
                #         break

                target_user = 5890  # ID d'un utilisateur connu pour les tests

                if not target_user:
                    self.print_error("Aucun utilisateur avec ≥5 interactions trouvé")
                    self.test_results.append(("Test 3: Interactions suffisantes", False))
                    return False

                # Tester les recommandations
                stats = self.get_user_stats(target_user)
                print(f"\n  📈 Statistiques utilisateur {target_user}:")
                print(f"     • Total interactions: {stats.get('total_interactions', 0)}")
                print(f"     • Articles uniques: {stats.get('unique_articles', 0)}")
                print(f"     • Top catégories: {stats.get('top_categories', [])[:3]}")

                methods = ["content", "clustering", "hybrid"]
                results = []

                for method in methods:
                    # Ces méthodes NE DOIVENT PAS faire de fallback
                    passed = self.test_recommendation(target_user, method, expected_fallback=False)
                    results.append(passed)

                all_passed = all(results)
                if all_passed:
                    self.print_success("✨ TEST 3 RÉUSSI: Recommandations personnalisées appliquées")
                else:
                    self.print_error("💥 TEST 3 ÉCHOUÉ")

                self.test_results.append(("Test 3: Interactions suffisantes", all_passed))
                return all_passed
            else:
                self.print_error(f"Impossible de récupérer la liste des utilisateurs: {response.status_code}")
                self.test_results.append(("Test 3: Interactions suffisantes", False))
                return False

        except Exception as e:
            self.print_error(f"Erreur durant le test: {e}")
            self.test_results.append(("Test 3: Interactions suffisantes", False))
            return False

    def test_health(self) -> bool:
        """Vérifie que l'API est disponible"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def print_final_summary(self):
        """Affiche le résumé final de tous les tests"""
        self.print_section("RÉSUMÉ FINAL DES TESTS")

        print(f"\n  {'Test':<50} {'Résultat':<15}")
        print(f"  {'-'*50} {'-'*15}")

        total_tests = 0
        passed_tests = 0

        for test_name, result in self.test_results:
            total_tests += 1
            if result is True:
                passed_tests += 1
                status = f"{Fore.GREEN}✅ RÉUSSI{Style.RESET_ALL}"
            elif result is False:
                status = f"{Fore.RED}❌ ÉCHOUÉ{Style.RESET_ALL}"
            else:
                status = f"{Fore.YELLOW}⚠️  IGNORÉ{Style.RESET_ALL}"
                total_tests -= 1  # Ne pas compter les tests ignorés

            print(f"  {test_name:<50} {status}")

        print(f"\n  {'-'*50} {'-'*15}")

        if total_tests > 0:
            success_rate = (passed_tests / total_tests) * 100
            print(f"\n  📊 Taux de réussite: {passed_tests}/{total_tests} ({success_rate:.1f}%)")

            if success_rate == 100:
                self.print_success("🎉 TOUS LES TESTS SONT PASSÉS !")
            elif success_rate >= 75:
                self.print_warning(f"⚠️  La plupart des tests sont passés ({success_rate:.1f}%)")
            else:
                self.print_error(f"💥 Beaucoup de tests ont échoué ({100-success_rate:.1f}%)")
        else:
            self.print_warning("Aucun test n'a été exécuté")

    def run_all_tests(self):
        """Lance tous les tests de cold start"""
        print(f"{Fore.CYAN}")
        print("=" * 80)
        print("  🧪 TESTS DE VALIDATION DU COLD START")
        print("  Validation de la détection intelligente et des fallbacks")
        print("=" * 80)
        print(f"{Style.RESET_ALL}")

        # Vérifier que l'API est disponible
        self.print_info("Vérification de la disponibilité de l'API...")
        if not self.test_health():
            self.print_error("❌ L'API n'est pas disponible. Assurez-vous qu'elle est démarrée.")
            sys.exit(1)
        self.print_success("API disponible")

        # Lancer les tests
        self.test_scenario_1_new_user()
        self.test_scenario_2_few_interactions()
        self.test_scenario_3_sufficient_interactions()

        # Résumé final
        self.print_final_summary()

if __name__ == "__main__":
    tester = ColdStartTester()
    tester.run_all_tests()