import streamlit as st

# === PAGE 2 : Implémentation RAG ===
def rag_implementation():
    """Affiche la page d'implémentation RAG de l'application."""

    st.header("🔍 Implémentation RAG et Données Culinaires")
    st.markdown("""
    ### **📌 Contexte**
    Cette section explore comment nous avons implémenté la Génération Augmentée par Récupération (RAG) pour alimenter notre Assistant de Cuisine. RAG permet au chatbot d'accéder et d'utiliser une vaste base de connaissances d'informations culinaires, garantissant que ses réponses sont précises, pertinentes et informatives.

    ### **🎯 Objectif**
    Notre objectif principal avec RAG est d'améliorer la capacité du chatbot à :
    - Récupérer des recettes et des techniques de cuisine spécifiques.
    - Comprendre les requêtes des utilisateurs relatives aux ingrédients, aux cuisines et aux restrictions alimentaires.
    - Générer des réponses utiles et contextuellement appropriées.

    ---

    ### **⚙️ Comment ça Marche**
    L'implémentation RAG implique plusieurs étapes clés :
    1. **Ingestion des Données :** Nous collectons des données à partir du site marmiton, a l'aide d'un cooking scrapper qui scrape +460 site de cuisine.
    2. **Prétraitement des Données :** Les données collectées sont nettoyées, formatées et structurées en json pour une récupération efficace. Puis divise en chunk sans couper leur structure initiale.
    3. **Vectorisation :**  Nous avons essaye plusieurs techniques de vectorisation, nous avons choisis **text-embedding-004** avec un task type = **semantic_similarity** permettant des recherches de similarité sémantique.
    4. **Base de Données Vectorielle :** Les données vectorisées sont stockées dans une base de données **Chroma** qui est persistante.
    5. **Récupération :** Lorsqu'un utilisateur pose une question, le système récupère les informations les plus pertinentes de la base de données vectorielle puis les integre dans un prompt specifique a la cuisine.
    6. **Génération :** Les informations récupérées sont ensuite transmises à un Grand Modèle de Langage (LLM), qui génère une réponse cohérente et informative.

    ---

    ### **🛠️ Notre Approche**
    Nous utilisons une combinaison de techniques, notamment :

    - **Large Langage Model (LLM) :** gemini-2.0-flash, Mistral
    - **Bases de Données Vectorielles :** ChromaDB, Pinecone, Weaviate
    - **Web Scraping (Potentiellement) :** Pour collecter des données à partir de sites web de cuisine et de bases de données de recettes.

    Explorez les différentes sections de notre application pour voir l'Assistant de Cuisine en action ! 🚀
    """)
