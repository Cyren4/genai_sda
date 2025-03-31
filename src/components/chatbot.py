# src/components/chatbot.py

import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from chromadb import PersistentClient
import traceback
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings
from markdown import markdown

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    st.error("Clé API Google non trouvée. Veuillez la définir dans vos variables d'environnement (GOOGLE_API_KEY).")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# --- Configuration ChromaDB ---
pwd = os.getcwd()
CHROMA_DB_PATH = os.path.join(pwd, "data", "chroma_db_recipes")
COLLECTION_NAME = "marmiton_recipes"
EMBEDDING_MODEL = 'models/text-embedding-004' # Modèle utilisé pour les embeddings

# --- Configuration fonction d'embedding ---
class GoogleEmbeddingFunction(EmbeddingFunction):
    """Fonction d'embedding personnalisée pour Google GenAI."""
    def __call__(self, input: Documents) -> Embeddings:
        try:
            response = genai.embed_content(model=EMBEDDING_MODEL,
                                           content=input,
                                           task_type="retrieval_document") 
            if 'embedding' not in response:
                print(f"Error: 'embedding' key not found in response for input: {input[:50]}...") # Log partiel
                return [None] * len(input)
            return response['embedding']
        except Exception as e:
            print(f"Error during embedding generation: {e}")
            return [None] * len(input)


# --- Initialisation ChromaDB ---
@st.cache_resource
def get_chroma_collection():
    """Charge ou crée la collection ChromaDB avec la fonction d'embedding Google."""
    try:
        google_ef = GoogleEmbeddingFunction() # Instanciation simple
        client = PersistentClient(path=CHROMA_DB_PATH)

        db = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=google_ef # Fournir l'instance
        )

        print(f"Successfully connected to ChromaDB collection: {COLLECTION_NAME}")
        return db
    except Exception as e:
        st.error(f"Failed to connect to ChromaDB collection '{COLLECTION_NAME}': {e}")
        print(f"Error connecting to ChromaDB: {e}")
        st.stop() # Arrêter l'exécution si la DB n'est pas accessible

db = get_chroma_collection()

# --- Fonctions RAG ---

def get_relevant_passages(query, db, n_results=3):
    """Récupère les N passages les plus pertinents depuis ChromaDB."""
    if db is None:
        st.error("Erreur: La base de données ChromaDB n'est pas disponible.")
        return [], [] # Retourne des listes vides pour éviter des erreurs en aval
    try:
        query_embedding = genai.embed_content(model=EMBEDDING_MODEL,
                                              content=query,
                                              task_type="retrieval_query")['embedding']

        results = db.query(
            query_embeddings=[query_embedding], # Utilise l'embedding de la question
            n_results=n_results,
            include=['documents', 'metadatas', 'distances'] # Inclure documents, métadonnées et distances
        )

        # Vérifier la structure des résultats
        if results and results.get('documents') and results['documents'][0]:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0] if results.get('metadatas') else [{}] * len(documents)
            distances = results['distances'][0] if results.get('distances') else [None] * len(documents)

            print(f"Found {len(documents)} relevant passages.")
            return documents, metadatas, distances # Retourne la liste des documents et leurs métadonnées
        else:
            print("No relevant passages found in the database.")
            return [], []
    except Exception as e:
        st.error(f"Erreur lors de la recherche dans ChromaDB: {e}")
        print(f"Error querying ChromaDB: {e}")
        return [], []

def cook_prompt_with_context_and_history(query, relevant_passages, history):
    """Construit le prompt pour Gemini en utilisant RAG (multiples passages) et l'historique."""

    # Formatage de l'historique
    formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    # Formatage des passages pertinents
    context_str = ""
    if relevant_passages:
        context_str = "Voici des extraits de recettes qui pourraient être utiles:\n\n"
        for i, passage in enumerate(relevant_passages):
            escaped_passage = passage.replace("\n", " ")
            context_str += f"--- Recette Pertinente {i+1} ---\n{escaped_passage}\n\n"
    else:
        context_str = "Aucune recette spécifique trouvée dans la base de données pour cette question.\n"

    # Construction du prompt final
    prompt = f"""Historique de la conversation:
{formatted_history}

----
CONTEXTE FOURNI:
{context_str}
----

INSTRUCTIONS:
Tu es mon assistant culinaire Cooking AI, amical et serviable.
En te basant **uniquement** sur l'HISTORIQUE de la conversation et le CONTEXTE FOURNI ci-dessus, réponds à la dernière QUESTION de l'utilisateur.
Si le contexte ne contient pas la réponse ou n'est pas pertinent, indique que les informations fournies ne permettent pas de répondre précisément
mais essaie quand même d'aider en te basant sur l'historique si possible.
Ne mentionne PAS explicitement le "CONTEXTE FOURNI" ou les "Recettes Pertinentes" dans ta réponse finale, intègre l'information naturellement.
Sois détaillé et clair. Si tu utilises des informations d'une recette spécifique du contexte, tu peux mentionner son nom si disponible dans le contexte.
Donne moi plus details et retourne toute la recette en entier UNIQUEMENT si je le demande.

QUESTION: '{query}'

RÉPONSE:
"""
    return prompt

# --- Fonction Principale du Chatbot ---
def chatbot(): 
    """Affiche le composant chatbot dans Streamlit."""
    st.caption("Votre guide pour les cuistots du dimanche !")

    # --- Gestion de l'historique des chats (identique à votre code) ---
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y")
    chat_data_dir = 'chat_data'
    os.makedirs(chat_data_dir, exist_ok=True)

    past_chats_path = os.path.join(chat_data_dir, 'past_chats_list')
    try:
        past_chats: dict = joblib.load(past_chats_path)
    except FileNotFoundError:
        past_chats = {}
    except Exception as e:
        st.error(f"Erreur lors du chargement de la liste des chats: {e}")
        past_chats = {}

    max_incremental = -1
    today_chats_count = 0
    for chat_id in past_chats.keys():
        if chat_id.startswith(date_str):
            today_chats_count += 1
            try:
                parts = chat_id.split('#')
                if len(parts) > 1:
                    incremental = int(parts[1])
                    max_incremental = max(max_incremental, incremental)
            except (IndexError, ValueError):
                pass

    if today_chats_count > 0 and max_incremental == -1 :
        next_incremental = today_chats_count
    else:
        next_incremental = max_incremental + 1

    new_chat_id = f'{date_str} #{next_incremental:02d}'

    MODEL_ROLE = 'assistant' # Gemini utilise souvent 'model' ou 'assistant'
    USER_ROLE = 'user'
    AI_AVATAR_ICON = '🍳'

    with st.sidebar:
        st.write('# Sessions de Cuisine Passées')
        options = [new_chat_id] + sorted(list(past_chats.keys()), reverse=True)

        selected_index = 0
        if 'chat_id' in st.session_state and st.session_state.chat_id in options:
            try:
                selected_index = options.index(st.session_state.chat_id)
            except ValueError:
                st.session_state.chat_id = new_chat_id
                selected_index = 0
        elif 'chat_id' not in st.session_state :
            st.session_state.chat_id = new_chat_id
            selected_index = 0

        def format_chat_option(chat_id):
            if chat_id == new_chat_id and chat_id not in past_chats:
                return "✨ Nouvelle Session..."
            return past_chats.get(chat_id, chat_id)

        selected_chat_id = st.selectbox(
            label='Choisissez une session',
            options=options,
            index=selected_index,
            format_func=format_chat_option,
            key='chat_selector'
        )

        if selected_chat_id != st.session_state.get('chat_id'):
            st.session_state.chat_id = selected_chat_id
            # Effacer les messages lors du changement de chat pour forcer le rechargement
            if 'messages' in st.session_state:
                del st.session_state['messages']
            st.rerun()

        st.session_state.chat_title = past_chats.get(st.session_state.chat_id, f'Session {st.session_state.chat_id}')

        # --- Ajout du contrôle pour n_results ---
        num_chunks = st.number_input(
            "Nombre de recettes contextuelles (chunks) :",
            min_value=1,
            max_value=10, 
            value=1,      
            step=1,
            key='num_chunks_selector', 
            help="Combien de recettes similaires utiliser pour répondre à votre question."
        )
        st.session_state.n_results = num_chunks


    messages_path = os.path.join(chat_data_dir, f'{st.session_state.chat_id}-st_messages')

    if 'messages' not in st.session_state:
        print(f"Attempting to load messages for {st.session_state.chat_id} from {messages_path}")
        try:
            st.session_state.messages = joblib.load(messages_path)
            print(f"Loaded {len(st.session_state.messages)} messages for chat {st.session_state.chat_id}")
        except FileNotFoundError:
            print(f"No history file found for {st.session_state.chat_id}. Starting new history.")
            st.session_state.messages = [] # Commence un nouvel historique si fichier non trouvé
        except Exception as e:
            st.error(f"Erreur lors du chargement de l'historique pour {st.session_state.chat_id}: {e}")
            st.session_state.messages = []

    # Initialisation du modèle Gemini (mis en cache implicitement par Streamlit via session_state)
    if 'gemini_model' not in st.session_state:
        try:
             # Utiliser gemini-1.5-flash ou gemini-pro selon disponibilité/préférence
            st.session_state.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
            print("Gemini Model Initialized (gemini-2.0-flash)")
        except Exception as e:
            st.error(f"Impossible d'initialiser le modèle Gemini : {e}")
            st.stop()

    # Affichage des messages de l'historique (depuis st.session_state.messages)
    for message in st.session_state.get('messages', []):
        role = message.get('role')
        avatar = message.get('avatar')
        # Assurer la compatibilité : Gemini utilise 'user' et 'model'
        display_role = 'assistant' if role == MODEL_ROLE else role # Afficher 'assistant' pour le modèle
        if role and message.get('content'): # Vérifier que role et content existent
             with st.chat_message(name=display_role, avatar=avatar):
                st.markdown(message['content'])

    # --- Input utilisateur et logique RAG ---
    if prompt := st.chat_input('Posez-moi une question de cuisine...'):
        is_new_chat = st.session_state.chat_id == new_chat_id and not os.path.exists(messages_path)

        # Ajouter le nouveau chat à la liste si nécessaire
        if st.session_state.chat_id not in past_chats:
            current_chat_title = f'Session {st.session_state.chat_id}'
            st.session_state.chat_title = current_chat_title
            past_chats[st.session_state.chat_id] = current_chat_title
            try:
                joblib.dump(past_chats, past_chats_path)
                print(f"Saved new chat ID {st.session_state.chat_id} to list.")
            except Exception as e:
                st.error(f"Erreur lors de la sauvegarde de la liste des chats: {e}")

        # Afficher le message utilisateur et l'ajouter à l'historique de session
        with st.chat_message(USER_ROLE):
            st.markdown(prompt)
        st.session_state.messages.append({"role": USER_ROLE, "content": prompt})

        # --- Étape RAG ---
        n_results = st.session_state.get('n_results', 3) # Récupérer la valeur depuis session_state
        progress_bar = st.status(f"👩‍🍳 Recherche de {n_results} recette(s) pertinente(s)...")
        relevant_passages, metadatas, distances = get_relevant_passages(prompt, db, n_results=n_results)
        progress_bar.update(label="✅ Informations trouvées!" if relevant_passages else "⚠️ Aucune recette spécifique trouvée.")

        # Construire le prompt RAG en utilisant l'historique actuel (AVANT la réponse de l'IA)
        gemini_history = [
            {"role": "user" if msg["role"] == USER_ROLE else "model", "parts": [msg["content"]]}
            for msg in st.session_state.messages if msg["role"] in [USER_ROLE, MODEL_ROLE]
        ]
        # Simplification: on utilise le prompt construit directement
        final_prompt_text = cook_prompt_with_context_and_history(prompt, relevant_passages, st.session_state.messages)

        # --- Génération de la réponse IA ---
        try:
            # print("\n--- FINAL PROMPT FOR GEMINI ---") # Pour débogage
            # print(final_prompt_text)
            # print("--- END FINAL PROMPT ---\n")

            # Utiliser generate_content pour une requête unique (stateless)
            response = st.session_state.gemini_model.generate_content(
                 final_prompt_text,
                 stream=True)

            # Afficher la réponse de l'IA en streaming
            with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
                message_placeholder = st.empty()
                full_response_content = ''
                for chunk in response:
                    # Gérer les erreurs potentielles dans le chunk (ex: blocage de sécurité)
                    if not hasattr(chunk, 'text'):
                         if hasattr(chunk, 'prompt_feedback') and chunk.prompt_feedback.block_reason:
                             reason = chunk.prompt_feedback.block_reason
                             error_msg = f"⚠️ Contenu bloqué par les filtres de sécurité ({reason}). Réessayez avec une autre formulation."
                             print(error_msg)
                             full_response_content = error_msg # Afficher l'erreur
                             break # Sortir de la boucle de streaming
                         else:
                             print(f"Chunk non traité: {chunk}")
                             continue # Ignorer les chunks sans texte ou erreur connue

                    word_list = chunk.text.split(' ')
                    for word in word_list:
                        full_response_content += word + ' '
                        # time.sleep(0.05) # Simulation de frappe
                        message_placeholder.markdown(full_response_content + "▌")
                message_placeholder.markdown(full_response_content.strip()) # Affichage final

            # Ajouter la réponse de l'IA à l'historique de session
            st.session_state.messages.append(
                {"role": MODEL_ROLE, "content": full_response_content.strip(), "avatar": AI_AVATAR_ICON}
            )

            # --- Sauvegarde de l'historique mis à jour ---
            try:
                joblib.dump(st.session_state.messages, messages_path)
                # print(f"Saved updated chat history to: {messages_path}")
            except Exception as e:
                st.error(f"Erreur lors de la sauvegarde de l'historique du chat: {e}")

            # Afficher les sources utilisées dans un expander
            if relevant_passages:
                with st.expander("Sources utilisées pour la réponse"):
                    for i, (doc, meta) in enumerate(zip(relevant_passages, metadatas)):
                        title = meta.get('title', f'Source {i+1}') if meta else f'Source {i+1}'
                        distance = distances[i] 
                        st.info(f"**{title}** (Pertinence: {1-distance:.2f})\n\n_{doc[:250]}..._") # Affiche un aperçu


            # Si c'était un nouveau chat, rerun pour mettre à jour le selectbox
            if is_new_chat:
                st.rerun()

        except Exception as e:
            print(f"Une erreur est survenue: {e}")
            print("--- Traceback complet ---")
            traceback.print_exc()
            print("--- Fin Traceback ---")
        #     st.error(f"Une erreur est survenue lors de la génération de la réponse Gemini: {e}")
        #     print(f"Error during AI response generation: {e}")
        #     # Ajouter un message d'erreur à l'historique
        #     st.session_state.messages.append(
        #         {"role": MODEL_ROLE, "content": f"Désolé, une erreur s'est produite: {e}", "avatar": AI_AVATAR_ICON}
        #     )
        #     try:
        #         joblib.dump(st.session_state.messages, messages_path)
        #     except Exception as save_e:
        #         st.error(f"Erreur critique : impossible de sauvegarder l'historique après l'échec de la génération: {save_e}")

