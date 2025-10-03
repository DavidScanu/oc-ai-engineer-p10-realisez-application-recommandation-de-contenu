# **TODO**

- ✅ **Normaliser** sur la période d'existence de l'article (pour enlever le filtre de récence, 3 mois). Ex : si l’article à 8 mois, on divise par le nombre de mois.
- Ajouter un paramètre de nouveauté
- ✅ **Nouvel utilisateur** : Quand on entre un ID utilisateur qui n’existe pas, quelle méthode de recommandation ? Popularité.
- ✅ Explication de ce qu'il se passe en cas de nouvel utilisateur (cold start) et de nouvel article dans la documentation.
- ✅ Novelty score pour le cold start des articles 

- ✅ Ajouter un endpoint pour les articles récents (optionnel : filtrer par catégorie)
- Ajouter un endpoint pour les utilisateurs les plus actifs `/users/active?limit=20` (optionnel : filtrer par catégorie)
- Ajouter un endpoint pour les articles les plus populaires `/articles/popular?limit=20` (optionnel : filtrer par catégorie)

- Améliorer méthode de recommandation hybride
- Ajouter un paramètre de longueur moyenne des articles (pour les utilisateurs qui lisent des articles longs ou courts)
- Ajouter un paramètre de diversité
- Ajouter un paramètre de nouveauté (pour les utilisateurs qui lisent des articles récents ou anciens)
- Ajouter un paramètre de popularité (pour les utilisateurs qui lisent des articles populaires ou non populaires)
- Ajouter un paramètre de catégorie (pour les utilisateurs qui lisent des articles d'une certaine catégorie)

- Déploiement de l’application (Azure App Service, Vercel)
- Documentation du code et de l’application
- Présentation (Google Slides)