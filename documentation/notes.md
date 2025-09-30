# Projet 10 \- Notes

# **Objectif**

* Créer un moteur de recommandation.  
* Équilibre entre nouveauté et pertinence.

# **Modèle final** 

* Entrée : **ID Utilisateur** (ou IDs d’article)  
* Sortie : **Liste d’IDs d’articles** 

# **Méthodes**

1. **Content based** : Interaction de l’utilisateur (articles consultés) \-\> Similarité des embeddings  
   1. Calculer score de similitude (cosinus) \-\> ID d’article similaires (5 articles similaires)  
   2. Manque titre de l’article et le texte de l’article (Solution : API LLM qui résume/fabrique le titre de l’article)  
2. **Collaborative filtering** :  
   1. Option 1 :   
      1. Rapprochement des comportements des utilisateurs (Solution : Segmentation des utilisateurs)  
      2. Recommande des articles qu’un utilisateur similaire a consulté  
   2. Option 2 :  
      1. Recommande des articles souvent vus ensemble  
3. **RNN ou entraînement de modèles**   
   1. embeddings   
   2. Metadonnées des articles 

# **Infrastructure**

1. **Backend** : Azure Functions, Endpoint d’API   
2. **Frontend** : Local [Next.js](http://Next.js) / Streamlit

# **TODO**

- ✅ **Normaliser** sur la période d'existence de l'article (pour enlever le filtre de récence, 3 mois). Ex : si l’article à 8 mois, on divise par le nombre de mois.
- Ajouter un paramètre de nouveauté
- ✅ **Nouvel utilisateur** : Quand on entre un ID utilisateur qui n’existe pas, quelle méthode de recommandation ? Popularité.
- ✅ Explication de ce qu'il se passe en cas de nouvel utilisateur (cold start) et de nouvel article dans la documentation.
