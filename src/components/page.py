import streamlit as st
import os
from components.introduction import introduction
from components.rag_implementation import rag_implementation
from components.chatbot import chatbot
from components.architecture import architecture

#


def select_page(page):
    """Select the page to display based on the user's selection."""
    # Get dynamic path
    pwd = os.getcwd() 

    if page == "📖 Introduction to Webtoon Chatbot":
        introduction()
    elif page == "🔍 RAG Implementation and Webtoon Data":
        rag_implementation()
    elif page == "🤖 Chat with the Webtoon Assistant!":
        chatbot()
    elif page == "🏗️ Architecture":
        architecture()
