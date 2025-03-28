import streamlit as st

# Pop up content
about_message = """
### About Cooking Assistant Application

This application showcases a specialized chatbot designed to provide information and engage in conversations about cooking. It leverages Retrieval-Augmented Generation (RAG) to deliver accurate and relevant responses.

### Need help? Here's how to get in touch:

*   **Email Support:** support@cooking-assistant.com
*   **FAQ:** cooking-assistant.com/faq
*   **Documentation:** cooking-assistant.com/docs

Please include the following information when contacting support:
* A description of the problem you are experiencing.
* Screenshots (if applicable).
* The version of the application you are using.
"""

def display_header():
    st.title("🍳 Cooking Assistant: Your Guide to Culinary Creations")

def display_contributor():
    """Displays the contributors section of the app."""
    st.markdown("""
    ---

    ### 👩🏻‍🍳 **Contributors** :
    - *Cyrena Ramdani*
    - *Yoav COHEN*
    """)

# Page config
def page_config():
    st.set_page_config(
        page_title="Cooking Assistant",
        page_icon="🍳",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={
            'About': f"{about_message}"
        }
    )
