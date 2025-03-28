import streamlit as st

# === PAGE 2 : RAG Implementation ===
def rag_implementation():
    """Displays the rag page of the app."""

    st.header("🔍 RAG Implementation and Culinary Data")
    st.markdown("""
    ### **📌 Context**
    This section delves into how we've implemented Retrieval-Augmented Generation (RAG) to power our Cooking Assistant. RAG allows the chatbot to access and utilize a vast knowledge base of culinary information, ensuring that its responses are accurate, relevant, and informative.

    ### **🎯 Objective**
    Our primary goal with RAG is to enhance the chatbot's ability to:
    - Retrieve specific recipes and cooking techniques.
    - Understand user queries related to ingredients, cuisines, and dietary restrictions.
    - Generate helpful and contextually appropriate responses.

    ---

    ### **⚙️ How it Works**
    The RAG implementation involves several key steps:
    1. **Data Ingestion:** We gather data from various sources, including recipe websites, cooking blogs, and culinary databases.
    2. **Data Preprocessing:** The collected data is cleaned, formatted, and structured for efficient retrieval.
    3. **Vectorization:** We use advanced techniques to convert the text data into numerical vectors, allowing for semantic similarity searches.
    4. **Vector Database:** The vectorized data is stored in a specialized vector database, enabling fast and accurate retrieval.
    5. **Retrieval:** When a user asks a question, the system retrieves the most relevant information from the vector database.
    6. **Generation:** The retrieved information is then fed into a Large Language Model (LLM), which generates a coherent and informative response.

    ---

    ### **🛠️ Our Approach**
    We are using a combination of state-of-the-art techniques, including:

    - **Large Language Models (LLMs):** To understand and generate human-like text.
    - **Vector Databases:** To store and efficiently retrieve information about recipes and cooking techniques.
    - **Web Scraping (Potentially):** To gather data from cooking websites and recipe databases.

    Explore the different sections of our application to see the Cooking Assistant in action! 🚀
    """)
