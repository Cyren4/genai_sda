import streamlit as st
from components.header import display_header
from components.page import select_page


about_message = """
**Cooking AI **

Cette application est faites pour les plus flemmards d'entre nous\
qui non seulement n'ont pas la motivation de reflechir a quoi cuisiner \
mais aussi ont des competences culinaires limitees. 
""" 


def main():
    display_header()
    # === BARRE DE NAVIGATION ===
    st.sidebar.title("Navigation")
    main_page = st.sidebar.radio("Sélectionne une page",
                                  ["🍲 Introduction de Cooking AI",
                                   "🔍 Implémentation RAG et Données Culinaires",
                                   "🍳 Chat avec Cooking AI!",
                                   "🏗️ Architecture de Cooking AI"])
    select_page(main_page)
    # display_contributor()

if __name__ == "__main__":
    # st.set_page_config(
    #     page_title="Cooking Assistant",
    #     page_icon="🍳",
    #     layout="centered",
    #     initial_sidebar_state="auto",
    #     menu_items={
    #         'About': f"{about_message}" 
    #     }
    # )
    main()

