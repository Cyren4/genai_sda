import streamlit as st
# Import custom components
from components.header import  display_contributor

# === PAGE 1 : INTRODUCTION ===
def introduction():
    """Displays the INTRODUCTION page of the app."""

    st.header("🍲 Welcome to the Cooking Assistant!")

    st.markdown("""
    ### **📌 Context**
    Cooking can be a delightful journey, but it can also be challenging to find the right recipes, understand cooking techniques, or figure out what to make with the ingredients you have. That's where our Cooking Assistant comes in!

    ### **🎯 Objective**
    Our goal is to create a specialized chatbot that can:
    - Answer questions about specific recipes.
    - Recommend recipes based on user preferences and dietary restrictions.
    - Discuss cooking techniques, ingredients, and cuisines.
    - Provide insights into the culinary world.

    ---

    ### **⚙️ How it Works: RAG (Retrieval-Augmented Generation)**
    This chatbot is powered by RAG, a cutting-edge AI technique that combines the strengths of:
    - **Retrieval:** Searching a knowledge base for relevant recipes and cooking information.
    - **Generation:** Using a language model to create human-like responses and recipe suggestions.

    By grounding its responses in real-world data, the chatbot can provide accurate and informative answers.

    ---

    ### **🛠️ Our Approach**
    We are using a combination of state-of-the-art techniques, including:

    - **Large Language Models (LLMs):** To understand and generate human-like text.
    - **Vector Databases:** To store and efficiently retrieve information about recipes and cooking techniques.
    - **Web Scraping (Potentially):** To gather data from cooking websites and recipe databases.

    Explore the different sections of our application to see the Cooking Assistant in action! 🚀
    """)
    display_contributor()
