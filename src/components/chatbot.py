import streamlit as st

# === PAGE 3 : Chatbot ===
def chatbot():
    """Displays the chat page of the app."""

    st.header("🍳 Chat with the Cooking Assistant!")
    st.markdown("""
    ### **📌 Context**
    Welcome to the interactive chat section of our Cooking Assistant! Here, you can ask questions, seek recipe recommendations, and explore the world of cooking.

    ### **🎯 Objective**
    Our goal is to provide you with a seamless and informative cooking experience. Feel free to ask about:
    - Specific recipes or cooking techniques.
    - Ingredient substitutions or dietary restrictions.
    - Meal planning or culinary inspiration.

    ---

    ### **⚙️ How to Use**
    1. **Type your question or request** in the text box below.
    2. **Press Enter** or click the "Send" button.
    3. **Review the response** from the Cooking Assistant.
    4. **Continue the conversation** by asking follow-up questions or exploring new topics.

    ---

    ### **🛠️ Example Questions**
    - "What's a good recipe for chicken stir-fry?"
    - "How do I make a vegan chocolate cake?"
    - "What are some healthy breakfast ideas?"
    - "Can I substitute olive oil for butter in baking?"
    - "What are the best spices for Indian cuisine?"

    ---
    """)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What's cooking?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response = "I'm still learning how to cook, but I'm sure I can help you with that!"
            full_response += response
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
