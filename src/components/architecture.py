import streamlit as st

# === PAGE 4 : Architecture ===
def architecture():
    """Affiche la page d'architecture de l'application."""

    st.header("🏗️ Architecture de l'Assistant Culinaire")
    st.markdown("""
    ### **📌 Contexte**
    Cette section fournit une vue d'ensemble de haut niveau de l'architecture système qui alimente notre Assistant Culinaire. Comprendre l'architecture peut vous aider à apprécier la complexité et la sophistication de la technologie sous-jacente.

    ### **🎯 Objectif**
    Notre objectif est de créer une architecture robuste et évolutive qui peut :
    - Gérer et récupérer efficacement de grandes quantités de données culinaires.
    - S'intégrer de manière transparente avec les Grands Modèles de Langage (LLMs).
    - Fournir une expérience de chatbot réactive et conviviale.

    ---

    ### **⚙️ Composants Clés**
    1. **Sources de Données :**
        - Sites web et bases de données de recettes.
        - Blogs et forums de cuisine.
        - Livres et articles culinaires.
    2. **Ingestion et Prétraitement des Données :**
        - Outils de web scraping (si nécessaire).
        - Scripts de nettoyage et de formatage des données.
    3. **Base de Données Vectorielle :**
        - Une base de données spécialisée pour stocker les données culinaires vectorisées.
    4. **Grand Modèle de Langage (LLM) :**
        - Un LLM puissant pour comprendre et générer du texte.
    5. **Moteur RAG (Génération Augmentée par Récupération) :**
        - Le composant central qui combine la récupération et la génération.
    6. **Interface de Chatbot :**
        - L'application Streamlit qui fournit l'interface utilisateur.

    ---

    ### **🛠️ Flux de Données**
    1. Les données sont ingérées à partir de diverses sources.
    2. Les données sont prétraitées et vectorisées.
    3. Les données vectorisées sont stockées dans la base de données vectorielle.
    4. L'entrée de l'utilisateur est reçue via l'interface du chatbot.
    5. Le moteur RAG récupère les informations pertinentes de la base de données vectorielle.
    6. Le LLM génère une réponse basée sur les informations récupérées.
    7. La réponse est affichée à l'utilisateur via l'interface du chatbot.

    ---
    """)