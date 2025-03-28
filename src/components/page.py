import streamlit as st
import os
from components.introduction import introduction
from components.rag_implementation import rag_implementation
from components.chatbot import chatbot
from components.architecture import architecture

#


def select_page(page):
    """
    Selects and displays the appropriate page content based on the user's selection.

    This function acts as a router, directing the user to the correct section of the application
    based on their choice from the sidebar or navigation menu. It dynamically calls the relevant
    function to render the content for each page.

    Args:
        page (str): The name of the page selected by the user.

    """
    # Get dynamic path
    pwd = os.getcwd()

    if page == "🍲 Introduction to Cooking Assistant":
        introduction()
    elif page == "🔍 RAG Implementation and Culinary Data":
        rag_implementation()
    elif page == "🍳 Chat with the Cooking Assistant!":
        chatbot()
    elif page == "🏗️ Architecture of the Cooking Assistant":
        architecture()
