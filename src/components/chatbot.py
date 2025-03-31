import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from chromadb import PersistentClient,EmbeddingFunction, Documents, Embeddings
from markdown import markdown 

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# --- Configuration ChromaDB ---
pwd = os.getcwd()
CHROMA_DB_PATH = f"{pwd}/data/chroma2"
COLLECTION_NAME = "marmiton" 


# --- Configuration fonction d'embedding ---
class GoogleEmbeddingFunction(EmbeddingFunction):
  def __call__(self, input: Documents) -> Embeddings:
    model = 'models/text-embedding-004'
    # title = "Custom query"
    return genai.embed_content(model=model,
                                content=input,
                                task_type="semantic_similarity"  #retrieval_document,
                                # title=title
                                )["embedding"]

# --- Initialisation ChromaDB  ---
@st.cache_resource
def get_chroma_collection():
    try:
        # modele bd = 'models/text-embedding-004'  (768 dimensions).
        # to update si autre modèle
        google_ef = GoogleEmbeddingFunction(api_key=GOOGLE_API_KEY, model_name="models/text-embedding-004")

        client = PersistentClient(path=CHROMA_DB_PATH)

        # Passer la fonction d'embedding lors de la récupération de la collection
        db = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=google_ef 
        )

        print(f"Successfully connected to ChromaDB collection: {COLLECTION_NAME} using Google Embeddings 004 (768 dim)")
        return db
    except Exception as e:
        st.error(f"Failed to connect to ChromaDB with specified embedding function: {e}")
        print(f"Error connecting to ChromaDB: {e}")
        st.stop()


db = get_chroma_collection()

# updater n_results si on veut plus de resultats
def get_relevant_passage(query, db, n_results=4):
    """Récupère le passage le plus pertinent depuis ChromaDB."""
    if db is None:
        return "Erreur: La base de données ChromaDB n'est pas disponible."
    try:
        results = db.query(query_texts=[query], n_results=n_results)
        if results and results.get('documents') and results['documents'][0]:
            return results['documents'][0][0]
        else:
            return "Aucun passage pertinent trouvé dans la base de données."
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return f"Erreur lors de la recherche dans ChromaDB: {e}"

def cook_prompt(query, relevant_passage, history):
    """Construit le prompt pour le modèle GenAI en utilisant le contexte RAG et l'historique."""
    escaped_passage = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")

    # Formatage simple de l'historique
    formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    prompt = f"""Historique de la conversation:
{formatted_history}

----
Parlons cuisine ! Tu es mon assistant culinaire amical et serviable.
Base-toi UNIQUEMENT sur le PASSAGE suivant pour répondre à la QUESTION. Si le passage ne contient pas la réponse, indique que tu ne peux pas répondre avec les informations fournies. Ne mentionne pas explicitement le "PASSAGE" dans ta réponse finale. Donne autant de détails que possible issus du passage.

PASSAGE: '{escaped_passage}'

QUESTION: '{query}'

ANSWER:
"""
    return prompt

# --- Fonction Principale du Chatbot ---
def chatbot():
    # Get the current date
    now = datetime.now()
    date_str = now.strftime("%d-%m-%Y") # Format: DDMMYYYY

    # Create a chat_data/ folder if it doesn't already exist
    chat_data_dir = 'chat_data'
    os.makedirs(chat_data_dir, exist_ok=True) # Plus sûr que try/except

    # Load past chats list (if available)
    past_chats_path = os.path.join(chat_data_dir, 'past_chats_list')
    try:
        past_chats: dict = joblib.load(past_chats_path)
    except FileNotFoundError:
        past_chats = {}
    except Exception as e:
        st.error(f"Erreur lors du chargement de la liste des chats: {e}")
        past_chats = {}


    # Trouver le prochain numéro incrémental pour la date actuelle (logique simplifiée)
    # Attention: cette logique peut avoir des collisions si l'app redémarre vite.
    # Une approche plus robuste pourrait utiliser des timestamps ou UUIDs.
    # La logique originale est conservée pour la démonstration.
    max_incremental = -1
    today_chats_count = 0
    for chat_id in past_chats.keys():
        if chat_id.startswith(date_str):
            today_chats_count += 1
            try:
                # Extrait le numéro après '#' s'il existe
                parts = chat_id.split('#')
                if len(parts) > 1:
                   incremental = int(parts[1])
                   max_incremental = max(max_incremental, incremental)
            except (IndexError, ValueError):
                 pass # Ignore les chat_ids mal formés

    # Si aucun chat aujourd'hui, commence à 0, sinon prend le max + 1
    # Si des chats existent mais sans '#', on compte juste et on met max+1
    if today_chats_count > 0 and max_incremental == -1 : # Chats existent mais sans '#'
         next_incremental = today_chats_count
    else:
         next_incremental = max_incremental + 1

    new_chat_id = f'{date_str} #{next_incremental:02d}' # Format: DD-MM-YYYY #00


    MODEL_ROLE = 'ai'
    AI_AVATAR_ICON = '🍳' # Changé pour un thème cuisine

    # Sidebar pour la liste des chats passés
    with st.sidebar:
        st.write('# Sessions de Cuisine Passées')

        # Construction des options pour selectbox
        options = [new_chat_id] + sorted(list(past_chats.keys()), reverse=True) # Trié par date/numéro descendant

        # Détermine l'index sélectionné
        selected_index = 0 # Par défaut: Nouveau Chat
        if 'chat_id' in st.session_state and st.session_state.chat_id in options:
             # Si un chat ID existe déjà et est valide, le sélectionner
             try:
                 selected_index = options.index(st.session_state.chat_id)
             except ValueError:
                 # Si l'ID sauvegardé n'est plus dans les options (peu probable), revient au nouveau chat
                 st.session_state.chat_id = new_chat_id
                 selected_index = 0
        elif 'chat_id' not in st.session_state :
             # Premier chargement, initialise avec new_chat_id
             st.session_state.chat_id = new_chat_id
             selected_index = 0


        # Fonction pour formater l'affichage dans le selectbox
        def format_chat_option(chat_id):
            if chat_id == new_chat_id and chat_id not in past_chats:
                return "✨ Nouvelle Session..."
            # Essaye de récupérer le titre, sinon utilise l'ID
            return past_chats.get(chat_id, chat_id)


        # Le selectbox
        selected_chat_id = st.selectbox(
            label='Choisissez une session',
            options=options,
            index=selected_index,
            format_func=format_chat_option,
            key='chat_selector' # Ajout d'une clé explicite
        )

        # Met à jour le chat_id dans st.session_state SEULEMENT s'il change
        if selected_chat_id != st.session_state.get('chat_id'):
            st.session_state.chat_id = selected_chat_id
            # Forcer le rechargement si l'ID change pour charger le bon historique
            st.rerun()


        # Titre par défaut ou basé sur le premier message (ou laisser l'utilisateur nommer)
        # Ici, on garde un titre simple basé sur l'ID pour l'instant
        st.session_state.chat_title = past_chats.get(st.session_state.chat_id, f'Session {st.session_state.chat_id}')


    # --- Chargement de l'historique du chat sélectionné ---
    messages_path = os.path.join(chat_data_dir, f'{st.session_state.chat_id}-st_messages')
    try:
        # Vérifie si le chat sélectionné est un nouveau chat qui n'a pas encore de fichier
        if st.session_state.chat_id == new_chat_id and not os.path.exists(messages_path):
             st.session_state.messages = []
             print(f"Starting new chat: {st.session_state.chat_id}")
        else:
             st.session_state.messages = joblib.load(messages_path)
             print(f"Loaded chat history for: {st.session_state.chat_id}")
    except FileNotFoundError:
         # Si on sélectionne un ancien chat dont le fichier a disparu
         st.warning(f"Historique non trouvé pour {st.session_state.chat_id}. Un nouveau chat sera créé avec cet ID.")
         st.session_state.messages = []
         # Potentiellement retirer l'ID de past_chats s'il n'y a plus de fichier?
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'historique du chat {st.session_state.chat_id}: {e}")
        st.session_state.messages = [] # Recommence avec un historique vide en cas d'erreur

    # Initialisation du modèle GenAI (peut être mis en cache aussi si nécessaire)
    if 'model' not in st.session_state:
        st.session_state.model = genai.GenerativeModel('gemini-1.5-flash') # Modèle cohérent avec l'exemple RAG
        print("GenAI Model Initialized")


    # Affichage des messages de l'historique
    for message in st.session_state.get('messages', []): # Utilise .get pour éviter erreur si 'messages' n'existe pas encore
        avatar = message.get('avatar')
        with st.chat_message(name=message['role'], avatar=avatar):
            st.markdown(message['content'])

    # --- Input utilisateur et logique RAG ---
    if prompt := st.chat_input('Posez-moi une question de cuisine...'):
        # Sauvegarde l'ID et le titre du nouveau chat dès le premier message
        is_new_chat = st.session_state.chat_id not in past_chats
        if is_new_chat:
            # Utilise un titre initial, pourrait être amélioré (ex: basé sur le premier prompt)
            # Attention : S'assurer que le titre est défini avant de sauvegarder.
            current_chat_title = f'Session {st.session_state.chat_id}' # Titre initial
            st.session_state.chat_title = current_chat_title
            past_chats[st.session_state.chat_id] = current_chat_title
            try:
                joblib.dump(past_chats, past_chats_path)
                print(f"Saved new chat ID {st.session_state.chat_id} to list.")
            except Exception as e:
                 st.error(f"Erreur lors de la sauvegarde de la liste des chats: {e}")


        # Afficher le message de l'utilisateur
        with st.chat_message('user'):
            st.markdown(prompt)

        # Ajouter le message utilisateur à l'historique de session Streamlit
        st.session_state.messages.append(dict(role='user', content=prompt))

        # --- Étape RAG ---
        st.write("👩‍🍳 Recherche d'informations pertinentes...") # Indicateur visuel
        relevant_passage = get_relevant_passage(prompt, db)
        st.write("✅ Informations trouvées!") # Ou un message d'erreur/avertissement si rien n'est trouvé

        # Construire le prompt RAG en utilisant l'historique actuel (avant la réponse de l'IA)
        rag_prompt = cook_prompt(prompt, relevant_passage, st.session_state.messages)
        # print("\n--- RAG PROMPT ---") # Pour débogage
        # print(rag_prompt)
        # print("--- END RAG PROMPT ---\n")

        # --- Génération de la réponse IA ---
        try:
            response = st.session_state.model.generate_content(rag_prompt, stream=True)

            # Afficher la réponse de l'IA en streaming
            with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
                message_placeholder = st.empty()
                full_response_content = ''
                # Itérer sur les chunks de la réponse streamée
                for chunk in response:
                     # Vérifier si le chunk contient du texte (pour éviter erreurs si chunk vide ou autre type)
                     if hasattr(chunk, 'text'):
                         # Simuler l'effet de frappe (optionnel)
                         for word in chunk.text.split(' '):
                             full_response_content += word + ' '
                             time.sleep(0.05)
                             message_placeholder.markdown(full_response_content + "▌") # Afficher avec curseur
                     else:
                         # Gérer le cas où un chunk n'a pas de 'text' (peut arriver en fin de stream ou erreur)
                         print(f"Received chunk without text: {chunk}")

                # Afficher la réponse complète sans le curseur
                message_placeholder.markdown(full_response_content.strip()) # .strip() pour enlever espace final

            # Ajouter la réponse complète de l'IA à l'historique Streamlit
            st.session_state.messages.append(
                dict(
                    role=MODEL_ROLE,
                    content=full_response_content.strip(), # Utiliser le contenu accumulé
                    avatar=AI_AVATAR_ICON,
                )
            )

            # --- Sauvegarde de l'historique mis à jour ---
            try:
                joblib.dump(st.session_state.messages, messages_path)
                print(f"Saved updated chat history to: {messages_path}")
            except Exception as e:
                 st.error(f"Erreur lors de la sauvegarde de l'historique du chat: {e}")

            # Si c'était un nouveau chat, et qu'on veut rafraichir la sidebar
            # pour qu'il apparaisse correctement nommé et sélectionné.
            if is_new_chat:
                # Mettre à jour l'état pour que le selectbox se mette à jour au prochain tour
                st.rerun()


        except Exception as e:
            st.error(f"Une erreur est survenue lors de la génération de la réponse: {e}")
            print(f"Error during AI response generation: {e}")
            # Optionnel : ajouter un message d'erreur à l'historique
            st.session_state.messages.append(
                 dict(
                     role=MODEL_ROLE,
                     content=f"Désolé, une erreur s'est produite: {e}",
                     avatar=AI_AVATAR_ICON,
                 )
            )
             # Essayer de sauvegarder même après l'erreur (pour conserver le prompt utilisateur)
            try:
                joblib.dump(st.session_state.messages, messages_path)
            except Exception as save_e:
                 st.error(f"Erreur critique : impossible de sauvegarder l'historique après l'échec de la génération: {save_e}")

