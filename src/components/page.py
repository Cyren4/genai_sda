import streamlit as st
import os
from components.introduction import introduction
from components.rag_implementation import rag_implementation
from components.chatbot import chatbot
from components.architecture import architecture


def select_page(page):
    """
    Sélectionne et affiche le contenu de la page appropriée en fonction de la sélection de l'utilisateur.
    """
    # Obtenir le chemin dynamique
    pwd = os.getcwd()

    if page == "🍲 Introduction de Cooking AI":
        introduction()
    elif page == "🔍 Implémentation RAG et Données Culinaires":
        rag_implementation() 
    elif page == "🍳 Chat avec Cooking AI!":
        chatbot()
    elif page == "🏗️ Architecture de Cooking AI":
        architecture()
