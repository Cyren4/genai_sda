import streamlit as st

# === PAGE 1 : INTRODUCTION ===
def introduction():
    """Displays the INTRODUCTION page of the app."""

    st.header("📖 Welcome to the Webtoon Chatbot!")

    st.markdown("""
    ### **📌 Context**
    Webtoons have exploded in popularity, offering a vast library of diverse stories and art styles. Navigating this world can be overwhelming, and that's where our Webtoon Chatbot comes in!

    ### **🎯 Objective**
    Our goal is to create a specialized chatbot that can:
    - Answer questions about specific webtoons.
    - Recommend webtoons based on user preferences.
    - Discuss webtoon genres, trends, and creators.
    - Provide insights into the webtoon industry.

    ---

    ### **⚙️ How it Works: RAG (Retrieval-Augmented Generation)**
    This chatbot is powered by RAG, a cutting-edge AI technique that combines the strengths of:
    - **Retrieval:** Searching a knowledge base for relevant information.
    - **Generation:** Using a language model to create human-like responses.

    By grounding its responses in real-world data, the chatbot can provide accurate and informative answers.

    ---

    ### **🛠️ Our Approach**
    We are using a combination of state-of-the-art techniques, including:

    - **Large Language Models (LLMs):** To understand and generate human-like text.
    - **Vector Databases:** To store and efficiently retrieve information about webtoons.
    - **Web Scraping (Potentially):** To gather data from webtoon platforms.

    Explore the different sections of our application to see the Webtoon Chatbot in action! 🚀
    """)
