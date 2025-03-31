# import libraries
import streamlit as st
# Import custom components
from components.header import display_header, display_contributor, page_config
from components.page import select_page

# === CONFIGURATION DE LA PAGE ===
def main():
    """Main function to run the Streamlit app."""

    # === CONFIGURATION MLflow ===
    page_config()
    display_header()
    # === BARRE DE NAVIGATION ===
    st.sidebar.title("Navigation")
    main_page = st.sidebar.radio("Sélectionne une page",
                                  ["🍲 Introduction de Cooking AI",
                                   "🔍 Implémentation RAG et Données Culinaires",
                                   "🍳 Chat avec Cooking AI!",
                                   "🏗️ Architecture de Cooking AI"])
    # select_page(main_page, run_ID)
    select_page(main_page)
    # display_contributor()


if __name__ == "__main__":
    main()
