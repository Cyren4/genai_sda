import streamlit as st

# Contenu de la fenêtre contextuelle
about_message = """
### À propos de l'application Cooking Assistant

Cette application présente un chatbot spécialisé conçu pour fournir des informations et engager des conversations sur la cuisine. Il utilise la Génération Augmentée par Récupération (RAG) pour fournir des réponses précises et pertinentes.

### Besoin d'aide ? Voici comment nous contacter :

*   **Support par e-mail :** support@cooking-assistant.com
*   **FAQ :** cooking-assistant.com/faq
*   **Documentation :** cooking-assistant.com/docs

Veuillez inclure les informations suivantes lorsque vous contactez le support :
* Une description du problème que vous rencontrez.
* Des captures d'écran (si applicable).
* La version de l'application que vous utilisez.
"""

def display_header():
    st.header("🍳 Cooking AI : Guide pour les cuistots du dimanche")

def display_contributor():
    """Affiche la section des contributeurs de l'application."""
    st.markdown("""
    ---

    ### 👩🏻‍🍳 **Contributeurs** :
    - *Cyrena Ramdani*
    - *Yoav COHEN*
    """)


# === PAGE 3 : Chatbot ===
# def chatbot():

    # st.markdown("""
    # ### **📌 Contexte**
    # Bienvenue dans la section de chat interactif de notre Cooking Assistant ! Ici, vous pouvez poser des questions, demander des recommandations de recettes et explorer le monde de la cuisine.

    # ### **🎯 Objectif**
    # Notre objectif est de vous offrir une expérience culinaire fluide et informative. N'hésitez pas à poser des questions sur :
    # - Des recettes ou des techniques de cuisine spécifiques.
    # - Des substitutions d'ingrédients ou des restrictions alimentaires.
    # - La planification des repas ou l'inspiration culinaire.

    # ---

    # ### **⚙️ Comment utiliser**
    # 1. **Tapez votre question ou votre demande** dans la zone de texte ci-dessous.
    # 2. **Appuyez sur Entrée** ou cliquez sur le bouton "Envoyer".
    # 3. **Consultez la réponse** du Cooking Assistant.
    # 4. **Continuez la conversation** en posant des questions de suivi ou en explorant de nouveaux sujets.

    # ---

    # ### **🛠️ Exemples de questions**
    # - "Quelle est une bonne recette pour un sauté de poulet ?"
    # - "Comment faire un gâteau au chocolat végétalien ?"
    # - "Quelles sont les idées de petits déjeuners sains ?"
    # - "Puis-je remplacer le beurre par de l'huile d'olive dans la pâtisserie ?"
    # - "Quelles sont les meilleures épices pour la cuisine indienne ?"

    # ---
    # """)
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []

    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    # if prompt := st.chat_input("Qu'est-ce qui mijote ?"):
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     with st.chat_message("user"):
    #         st.markdown(prompt)

    #     with st.chat_message("assistant"):
    #         message_placeholder = st.empty()
    #         full_response = ""
    #         response = "J'apprends encore à cuisiner, mais je suis sûr de pouvoir vous aider avec ça !"
    #         full_response += response
    #         message_placeholder.markdown(full_response + "▌")
    #         message_placeholder.markdown(full_response)
    #     st.session_state.messages.append({"role": "assistant", "content": full_response})
