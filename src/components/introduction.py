import streamlit as st
# Import custom components
from components.header import display_contributor


# === PAGE 1 : INTRODUCTION ===
def introduction():
    """Affiche la page d'INTRODUCTION de l'application."""

    st.header("🍲 Bienvenue sur Cooking AI !")

    st.markdown("""
    ### **📌 Contexte**
    Cuisiner peut être un voyage délicieux, mais il peut aussi être difficile de trouver les bonnes recettes, de comprendre les techniques de cuisine ou de savoir quoi préparer avec les ingrédients dont vous disposez. C'est là que notre Assistant de Cuisine entre en jeu !

    ### **🎯 Objectif**
    Notre objectif est de créer un chatbot spécialisé capable de :
    - Répondre aux questions sur des recettes spécifiques.
    - Recommander des recettes en fonction des préférences des utilisateurs et des restrictions alimentaires.
    - Discuter des techniques de cuisine, des ingrédients et des cuisines.
    - Fournir des informations sur le monde culinaire.

    ---

    ### **⚙️ Comment ça Marche : RAG (Génération Augmentée par Récupération)**
    Ce chatbot est alimenté par RAG, une technique d'IA de pointe qui combine les forces de :
    - **Récupération :** Recherche dans une base de connaissances de recettes pertinentes et d'informations culinaires.
    - **Génération :** Utilisation d'un modèle de langage pour créer des réponses et des suggestions de recettes.

    En basant ses réponses sur des données du monde réel, le chatbot peut fournir des réponses précises et informatives.

    ---

    ### **🛠️ Notre Approche**
    Nous utilisons une combinaison de techniques de pointe, notamment :

    - **Large Language Model (LLM) :** Pour comprendre et générer du texte de type humain.
    - **Bases de Données Vectorielles :** Pour stocker et récupérer efficacement des informations sur les recettes et les techniques de cuisine que vous souhaitez.
    - **Web Scraping :** Pour collecter des données à partir de sites web de cuisine et de bases de données de recettes.

    Explorez les différentes sections de notre application pour voir l'Assistant de Cuisine en action ! 🚀
    """)
    display_contributor()
