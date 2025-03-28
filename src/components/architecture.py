import streamlit as st

# === PAGE 4 : Architecture ===
def architecture():
    """Displays the architecture page of the app."""

    st.header("🏗️ Architecture of the Cooking Assistant")
    st.markdown("""
    ### **📌 Context**
    This section provides a high-level overview of the system architecture that powers our Cooking Assistant. Understanding the architecture can help you appreciate the complexity and sophistication of the underlying technology.

    ### **🎯 Objective**
    Our goal is to create a robust and scalable architecture that can:
    - Efficiently manage and retrieve vast amounts of culinary data.
    - Seamlessly integrate with Large Language Models (LLMs).
    - Provide a responsive and user-friendly chatbot experience.

    ---

    ### **⚙️ Key Components**
    1. **Data Sources:**
        - Recipe websites and databases.
        - Cooking blogs and forums.
        - Culinary books and articles.
    2. **Data Ingestion and Preprocessing:**
        - Web scraping tools (if needed).
        - Data cleaning and formatting scripts.
    3. **Vector Database:**
        - A specialized database for storing vectorized culinary data.
    4. **Large Language Model (LLM):**
        - A powerful LLM for understanding and generating text.
    5. **RAG (Retrieval-Augmented Generation) Engine:**
        - The core component that combines retrieval and generation.
    6. **Chatbot Interface:**
        - The Streamlit application that provides the user interface.

    ---

    ### **🛠️ Data Flow**
    1. Data is ingested from various sources.
    2. Data is preprocessed and vectorized.
    3. Vectorized data is stored in the vector database.
    4. User input is received through the chatbot interface.
    5. The RAG engine retrieves relevant information from the vector database.
    6. The LLM generates a response based on the retrieved information.
    7. The response is displayed to the user through the chatbot interface.

    ---
    """)
